"""
This file contains the driver for the NL3PDDL project.
"""

# Standard library imports
import os
import csv
import json
import logging
from typing import Any, Literal, Annotated
import multiprocessing as mp
from datetime import datetime

# External package imports
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing_extensions import TypedDict
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph
from langgraph.graph.message import add_messages

from nl3pddl.feedback_eval import val_evaluate, val_feedback

from .check_output import check_action_output, check_domain_output
from .gen_prompts import action_message, domain_template, init_msgs
from .dataset import Dataset
from .params import Params, action_names, domain_name, get_action_iteration_threshold, get_hde_iteration_threshold, param_grid

# Internal package imports
# import nl3pddl as n3p
# from nl3pddl import Dataset, Params


# This is a pydantic model that we force the LLM to output in
# the form of during the action generation phase.
class ActionSchema(BaseModel):
    """Always use this tool to structure your response to the user."""
    pddl_action: str = Field(description=\
        "String of raw typed STRIPS PDDL code for a single action \
        (:action name :parameters (...) :precondition (...) :effect (...))"
    )
    predicates: list[str] = Field(description=\
        "List of allowed predicates of the form \
        (name arg1 - type1 arg2 - type2 ...) from this action and \
        previous actions, adding any new predicates used in this action"
    )
    types: list[str] = Field(description=\
        "List of allowed types from this action and previous actions, \
        adding any new types used in this action"
    )


class DomainSchema(BaseModel):
    """Always use this tool to structure your response to the user."""
    pddl_domain: str = Field(description=
        "String of raw typed STRIPS PDDL code for an entire domain \
        (:domain name :requirements (...) :types (...) :predicates (...)\
        :functions (...) :action (...))")

# LangGraph State, this object keeps track of all state for a single experiment
class State(TypedDict):
    """ The LangGraph application State"""
    #Run ID, identifier for the experiment run, allows us to filter in langsmith
    run_id: str
    #LLM Message History
    messages: Annotated[list, add_messages]
    # The json object of the message returned by the model
    json_last: Any
    # The index of the action we are currently trying to write
    action_index: int
    # The current action has passed validation
    action_valid: bool
    # We are done and have constructed all actions
    actions_done: bool
    # List of good action outputs, this is a list of ActionSchema.
    # This becomes valid to use for domain construction after
    # the action generation phase
    actions : list[ActionSchema]
    # The domain we are currently working on is syntactically valid
    domain_syn_val: bool

    # Number of iterations we have done in the action generation phase
    action_iterations : int 

    # Exited without producing a valid action after exceeding the retry limit
    action_timeout : bool = False 
    action_timeout_cause : str = "" # Action that caused the timeout 

    # Number of iterations we have done in the HDE validation phase
    hde_iterations : int
    
    # Exited without producing a valid domain after exceeding the retry limit
    hde_timeout : bool = False 

    # The domain we are currently working on is HDE, and we can begin evaluating it.
    domain_hde_val: bool

    evals_passed: int = 0  # Number of evaluations passed
    total_evals: int = 0  # Total number of evaluations attempted

# Results file generation helpers ==============================================

# CSV header for the results file
RESULTS_HEADER = [
    "trial",
    "domain_path",
    "provider",
    "model",
    "give_pred_descriptions",
    "desc_class",
    "hde_runs",
    "hde_timeout",
    "action_timeout",
    "action_timeout_cause",
    "evals_passed",
    "total_evals",
    "domain_raw"
]

def gen_results(d : Dataset, p : Params, s : State) -> tuple:
    """
    Generates a tuple of results for the experiment, to be written to the
    results file.
    """
    return (
        s["run_id"],
        p.domain_path,
        p.provider,
        p.model,
        p.give_pred_descriptions,
        p.desc_class,
        s["hde_iterations"],
        s["hde_timeout"],
        s["action_timeout"],
        s["action_timeout_cause"],
        s["evals_passed"],
        s["total_evals"],
        s["json_last"].pddl_domain if s["json_last"] else ""
    )

# Experiments Helpers ==========================================================



def create_langgraph(d: Dataset, p: Params) -> CompiledStateGraph:
    """
    Creates a langgraph for a single experiment with the given
    experimental parameters.
    """
    model = init_chat_model(p.model, model_provider=p.provider, timeout=60, max_retries=3)
    action_model = model.with_structured_output(ActionSchema)
    domain_model = model.with_structured_output(DomainSchema)

    # Lang-graph nodes =========================================================

    def call_action_model(state: State):
        json_obj = action_model.invoke(state["messages"])
        raw = json.dumps(json_obj.model_dump())
        return {"messages": [AIMessage(raw)], "json_last": json_obj}

    def call_domain_model(state: State):
        json_obj = domain_model.invoke(state["messages"])
        raw = json.dumps(json_obj.model_dump())
        return {"messages": [AIMessage(raw)], "json_last": json_obj}

    def next_action(state: State):
        action_index = state["action_index"]
        actions_names = action_names(d, p)
        actions = state["actions"]
        if action_index >= len(actions_names):
            return {
                "actions_done": True,
                "actions" : actions + [state["json_last"]]
            }
        else:
            action_name = actions_names[action_index]
            return {
                "messages": [action_message(d, p, action_name)],
                "action_index" : action_index + 1,
                "actions" : actions + [state["json_last"]],
                "action_iterations" : 0
            }

    def check_action(state: State):
        res = check_action_output(state["json_last"])
        return {
            "messages": [res] if res else [],
            "action_valid" : res is None,
            "action_iterations" : state["action_iterations"] + 1
        }

    def build_domain(state: State):
        full_domain_raw = domain_template(
            domain_name(d, p),
            state["actions"]
        )
        return {
            "messages" : [HumanMessage(full_domain_raw)],
            "json_last": DomainSchema(**{"pddl_domain":full_domain_raw})
        }

    def check_domain(state: State):
        res = check_domain_output(state["json_last"])
        return {
            "messages": [res] if res else [],
            "domain_syn_val" : res is None,
            "hde_iterations" : state["hde_iterations"] + 1
        }

    def validate(state: State):
        res = val_feedback(d, p, state["json_last"].pddl_domain)
        return {
            "messages": [res] if res else [],
            "domain_hde_val" : res is None,
        }
        
    def action_timeout_node(state: State):
        actions_names = action_names(d, p)
        failed_action_name = actions_names[state["action_index"]]
        return {
            "action_timeout": True,
            "action_timeout_cause": failed_action_name,
        }
    
    def hde_timeout_node(state: State):
        return {
            "hde_timeout": True
        }
    
    def final_evaluation(state: State):
        res = val_evaluate(d, p, state["json_last"].pddl_domain)
        return {
            "evals_passed": res[0],
            "total_evals": res[1],
        }

    # Conditional Routing Helpers ==============================================

    def route_actions(state: State) ->\
    Literal['action_timeout_node', 'next_action', 'call_action_model']:
        if state["action_iterations"] >= get_action_iteration_threshold():
            return "action_timeout_node"
        elif state["action_valid"]:
            return "next_action"
        else:
            return "call_action_model"

    def route_actions_done(state: State) ->\
    Literal['build_domain', 'call_action_model']:
        if state["actions_done"]:
            return "build_domain"
        else:
            return "call_action_model"

    def route_domain_syn(state: State) ->\
    Literal['hde_timeout_node', 'validate', 'call_domain_model']:
        if state["hde_iterations"] >= get_hde_iteration_threshold():
            return "hde_timeout_node"
        elif state["domain_syn_val"]:
            return "validate"
        else:
            return "call_domain_model"


    def route_hde(state: State) ->\
    Literal['call_domain_model', 'final_evaluation']:
        if state["domain_hde_val"]:
            return "final_evaluation"
        else:
            return "call_domain_model"

    # Create the graph =========================================================
    graph_builder = StateGraph(State)
    graph_builder.add_node("call_action_model", call_action_model)
    graph_builder.add_node("check_action", check_action)
    graph_builder.add_node("next_action", next_action)
    graph_builder.add_node("build_domain", build_domain)
    graph_builder.add_node("call_domain_model", call_domain_model)
    graph_builder.add_node("check_domain", check_domain)
    graph_builder.add_node("validate", validate)
    graph_builder.add_node("action_timeout_node", action_timeout_node)
    graph_builder.add_node("hde_timeout_node", hde_timeout_node)
    graph_builder.add_node("final_evaluation", final_evaluation)

    graph_builder.add_edge(START, "call_action_model")
    graph_builder.add_edge("call_action_model", "check_action")
    graph_builder.add_conditional_edges("check_action", route_actions)
    graph_builder.add_conditional_edges("next_action", route_actions_done)
    graph_builder.add_edge("build_domain", "check_domain")
    graph_builder.add_edge("call_domain_model", "check_domain")
    graph_builder.add_conditional_edges("check_domain", route_domain_syn)
    graph_builder.add_conditional_edges("validate", route_hde)
    graph_builder.add_edge("action_timeout_node", END)
    graph_builder.add_edge("hde_timeout_node", "final_evaluation")
    graph_builder.add_edge("final_evaluation", END)

    return graph_builder.compile()

def run_experiment(
    d: Dataset,     # Dataset
    p: Params,      # Experiment Parameters
    #results_lock,   # Lock on results file for thread safety
    batch_id : str,  # Identifier for the batch of experiments
    #results_path: str  # File to write results to
) -> dict:
    """
    Executes a LangGraph for a single experiment, and writes results
    to the results file.
    """
    graph = create_langgraph(d, p)

    graph.get_graph().draw_png("graph.png")

    initial_state = {
        "run_id": batch_id,
        "messages": init_msgs(d, p),
        "action_index": 0,
        "json_last": None,
        "action_valid": False,
        "actions_done": False,
        "actions" : [],
        "domain_syn_val": False,
        "domain_hde_val": False,
        "action_iterations" : 0,
        "hde_iterations" : 0,
        "action_timeout" : False,
        "action_timeout_cause" : "",
        "hde_timeout" : False,
        "evals_passed": 0,
        "total_evals": 0,
    }
    step = initial_state

    # Set the recursion limit for the graph execution to be high enough to 
    # accommodate the worst case scenario
    config = {
        "recursion_limit": 
            len(d.domains[p.domain_path].actions) * 
            get_action_iteration_threshold() + 
            get_hde_iteration_threshold() * 3 + 25,
    }

    try:
        logging.info("Running graph for %s", repr(p))
        for step in graph.stream(initial_state, stream_mode="values", config=config):
            continue
    except Exception as e: # pylint: disable=broad-except
        print (f"Error: {e}")
    res = gen_results(d, p, step)
    return res

def run_experiment_star(
    args: tuple[Dataset, Params, str]  # Dataset, Params, Batch ID
) -> dict:
    """
    Wrapper for run_experiment to unpack the arguments.
    This is used for multiprocessing.
    """
    return run_experiment(*args)

def experiment() -> None:
    """
    Driver, runs the experiments in parallel using the parameter grid
    """
    load_dotenv()

    if not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY environment variable not set.\
                            Please set it in your .env file.")
    if not os.environ.get("DEEPSEEK_API_KEY"):
        raise RuntimeError("DEEPEEK_API_KEY environment variable not set.\
                            Please set it in your .env file.")

    logging.getLogger().setLevel(logging.INFO)

    dataset = Dataset()

    date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    results_path = f'results/results-{date}.csv'
    with open(results_path, 'w', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(RESULTS_HEADER)

    args = [(dataset, params, date) for params in param_grid(dataset)]
    with mp.Pool(processes=None) as pool:
        with open(results_path, 'a', encoding="utf-8") as res_file:
            csv_writer = csv.writer(res_file)
            for v in pool.imap(run_experiment_star, args):
                csv_writer.writerow(v)
    print("Successfully joined all processes.")