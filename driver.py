"""
This file contains the driver for the NL3PDDL project.
It uses LangGraph to 
"""

# Standard library imports
import os
import csv
import json
import logging
from typing import Any, Literal, Annotated
import multiprocessing as mp

# External package imports
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing_extensions import TypedDict
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph
from langgraph.graph.message import add_messages

# Internal package imports
import nl3pddl as n3p
from nl3pddl import Dataset, Params

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

class State(TypedDict):
    """ The LangGraph application State"""
    #Run ID, identifier for the experiment run, allows us to filter in langsmith
    #TODO: populate this.
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
    # The domain we are currently working on is HDE
    domain_hde_val: bool
    # Number of iterations we have done in the action generation phase
    action_iterations : int
    # Number of iterations we have done in the HDE validation phase
    hde_iterations : int

ACTION_THRESHOLD = 5
VAL_THRESHOLD = 10

def create_langgraph(d: Dataset, p: Params) -> CompiledStateGraph:
    """
    Creates a langgraph for a single experiment with the given
    experimental parameters.
    """
    model = init_chat_model(p.model, model_provider=p.provider)
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
        actions_names = n3p.action_names(d, p)
        actions = state["actions"]
        if action_index >= len(actions_names):
            return {
                "actions_done": True,
                "actions" : actions + [state["json_last"]]
            }
        else:
            action_name = actions_names[action_index]
            return {
                "messages": [n3p.action_message(d, p, action_name)],
                "action_index" : action_index + 1,
                "actions" : actions + [state["json_last"]],
                "action_iterations" : 0
            }

    def check_action(state: State):
        res = n3p.check_action_output(state["json_last"])
        return {
            "messages": [res] if res else [],
            "action_valid" : res is None,
            "action_iterations" : state["action_iterations"] + 1
        }

    def build_domain(state: State):
        full_domain_raw = n3p.domain_template(
            n3p.domain_name(d, p),
            state["actions"]
        )
        return {
            "messages" : [HumanMessage(full_domain_raw)],
            "json_last": DomainSchema(**{"pddl_domain":full_domain_raw})
        }

    def check_domain(state: State):
        res = n3p.check_domain_output(state["json_last"])
        return {
            "messages": [res] if res else [],
            "domain_syn_val" : res is None
        }

    def validate(state: State):
        res = n3p.val_all(dataset, p, state["json_last"].pddl_domain)
        hde_iterations = state["hde_iterations"]
        return {
            "messages": [res] if res else [],
            "domain_hde_val" : res is None,
            "hde_iterations" : hde_iterations + 1
        }

    # Conditional Routing Helpers ==============================================

    def route_actions(state: State) ->\
    Literal['__end__', 'next_action', 'call_action_model']:
        if state["action_iterations"] >= ACTION_THRESHOLD:
            return END
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
    Literal['validate', 'call_domain_model']:
        if state["domain_syn_val"]:
            return "validate"
        else:
            return "call_domain_model"

    def route_hde(state: State) -> Literal['call_domain_model', '__end__']:
        if state["domain_hde_val"]:
            return END
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

    graph_builder.add_edge(START, "call_action_model")
    graph_builder.add_edge("call_action_model", "check_action")
    graph_builder.add_conditional_edges("check_action", route_actions)
    graph_builder.add_conditional_edges("next_action", route_actions_done)
    graph_builder.add_edge("build_domain", "check_domain")
    graph_builder.add_edge("check_domain", "validate")
    graph_builder.add_edge("call_domain_model", "check_domain")
    graph_builder.add_conditional_edges("check_domain", route_domain_syn)
    graph_builder.add_conditional_edges("validate", route_hde)

    return graph_builder.compile()

def run_experiment(
    d: Dataset,     # Dataset
    p: Params,      # Experiment Parameters
    results_lock    # Lock on results file for thread safety
) -> None:
    """
    Executes a LangGraph for a single experiment, and writes results
    to the results DataFrame.
    """
    graph = create_langgraph(d, p)

    initial_state = {
        "messages": n3p.init_msgs(d, p),
        "action_index": 0,
        "json_last": None,
        "action_valid": False,
        "actions_done": False,
        "actions" : [],
        "domain_syn_val": False,
        "domain_hde_val": False,
        "action_iterations" : 0,
        "hde_iterations" : 0
    }

    hde_iterations = 0
    action_iterations = 0

    try:
        logging.info("Running graph for %s", repr(p))
        for step in graph.stream(initial_state, stream_mode="values"):
            #step["messages"][-1].pretty_print()
            hde_iterations = step["hde_iterations"]
            action_iterations = step["action_iterations"]
    except Exception as e: # pylint: disable=broad-except
        print (f"Error: {e}")
    finally:
        results_lock.acquire()
        with open(r'results.csv', 'a', encoding="utf-8") as res_file:
            csv_writer = csv.writer(res_file)
            csv_writer.writerow(n3p.params_as_dict(
                p,
                hde_iterations,
                action_iterations
            ).values())
        results_lock.release()

if __name__ == "__main__":

    load_dotenv()

    if not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY environment variable not set.\
                            Please set it in your .env file.")
    if not os.environ.get("DEEPSEEK_API_KEY"):
        raise RuntimeError("DEEPEEK_API_KEY environment variable not set.\
                            Please set it in your .env file.")

    logging.getLogger().setLevel(logging.INFO)

    dataset = n3p.Dataset()

    #results_df = pd.DataFrame(columns=n3p.params_header())
    with open(r'results.csv', 'w', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(n3p.params_header())

    lock = mp.Lock()
    processes = []
    for params in n3p.param_grid(dataset):
        process = mp.Process(
            target=run_experiment,
            args=(dataset, params, lock)
        )
        processes.append(process)
        process.start()
    for process in processes:
        process.join()
    print("Successfully joined all processes.")

else:
    raise RuntimeError("This file is a driver for the NL3PDDL project. \
                        It should be run as a script, not imported.")
