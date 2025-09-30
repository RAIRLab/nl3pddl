"""
This file contains the driver for the NL3PDDL project.
"""

# Standard library imports
import os
import csv
import json
from typing import Any, Literal, Annotated
import multiprocessing as mp
from datetime import datetime

# External package imports
from pddl.parser.domain import DomainParser
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing_extensions import TypedDict
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph
from langgraph.graph.message import add_messages

from .config import THREADS
from .check_output import check_action_output, check_domain_syntax_output
from .gen_prompts import action_message, domain_template, init_msgs, raw_domain_msg
from .dataset import Dataset
from .params import Params, action_names, domain_name, feedback_pipeline_str, get_action_iteration_threshold, get_hde_iteration_threshold, param_grid
from .feedback_eval import single_landmark_feedback, val_evaluate, single_val_feedback
from .logger import logger

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
    # Experiment parameters, should not be modified during the run
    PARAMS: Params
    #LLM Message History up to the current tree level
    messages: Annotated[list, add_messages]
    #Proposed messages
    proposed: list[HumanMessage]
    proposed_responses: list[DomainSchema]
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
    domain_syntax_passed: bool

    # Number of iterations we have done in the action generation phase
    action_iterations : int 

    # Exited without producing a valid action after exceeding the retry limit
    action_timeout : bool = False 
    action_timeout_cause : str = "" # Action that caused the timeout 

    # feedback mode keeps track of what type of feedback we are
    # giving right now
    feedback_index : int = 0
    feedback_cycles : int = 0

    # number of times we have actually given landmark feedback to the model
    landmark_runs : int = 0

    # number of times we have given val feedback to the model
    val_runs : int = 0

    # The number of times we loop exclusively on syntax issues
    domain_check_runs : int = 0

    # Landmark node passed
    landmark_passed: bool = False

    # Total Number of iterations we have done in the HDE validation phase
    # This *actually* is a measure of how many times we have hit the 
    # domain syntax validator node, which is the number of times we have called
    # the language model + 1, see val_runs and landmark_runs for specific 
    # counts of types of feedback
    hde_iterations : int
    
    # Exited without producing a valid domain after exceeding the retry limit
    hde_timeout : bool = False 

    # The domain we are currently working on is HDE, and we can begin evaluating it.
    val_passed: bool = False

    evals_passed: int = 0  # Number of evaluations passed
    total_evals: int = 0  # Total number of evaluations attempted

    # Path of nodes taken through the langgraph, for debugging
    langgraph_path : list[str] = [] 

# Results file generation helpers ==============================================

# CSV header for the results file
RESULTS_HEADER = [
    "trial",
    "domain_path",
    "provider",
    "model",
    "give_pred_descriptions",
    "desc_class",
    "feedback_pipeline",
    "landmark_runs",
    "val_runs",
    "hde_runs",
    "hde_timeout",
    "action_timeout",
    "action_timeout_cause",
    "evals_passed",
    "total_evals",
    #"domain_raw"
]

def gen_csv_results(s : State) -> tuple:
    """
    Generates a tuple of results for the experiment, to be written to the
    results file, Requires that the experiment has completed successfully.
    needs to match the RESULTS_HEADER.
    """
    return (
        #s["run_id"],
        s["PARAMS"].trial,
        s["PARAMS"].domain_path,
        s["PARAMS"].provider,
        s["PARAMS"].model,
        s["PARAMS"].give_pred_descriptions,
        s["PARAMS"].desc_class,
        feedback_pipeline_str(s["PARAMS"]),
        s["landmark_runs"],
        s["val_runs"],
        s["hde_iterations"],
        s["hde_timeout"],
        s["action_timeout"],
        s["action_timeout_cause"],
        s["evals_passed"],
        s["total_evals"],
        #s["json_last"].pddl_domain if s["json_last"] else ""
    )

def write_message_log(s : State, err_msg : str, results_dir : str) -> None:
    """
    Writes the message log to a file in the results directory.
    """
    domain_path = s['PARAMS'].domain_path.split("/")[-1]
    log_path = os.path.join(results_dir, f"""{s['PARAMS'].provider}_{s['PARAMS'].model}_{domain_path}_{s['PARAMS'].desc_class}_{s['PARAMS'].trial}_{feedback_pipeline_str(s['PARAMS'])}_messages.log""")
    with open(log_path, 'w', encoding="utf-8") as f:

        f.write("NON VAR INFO =========================================\n\n")
        #f.write(f"RUN ID: {s['run_id']}\n")
        f.write(f"TRIAL: {s['PARAMS'].trial}\n")
        f.write("\nExperiment Params ====================================\n\n")
        f.write(f"PROVIDER: {s['PARAMS'].provider}\n")
        f.write(f"MODEL: {s['PARAMS'].model}\n")
        f.write(f"DOMAIN PATH: {s['PARAMS'].domain_path}\n")
        f.write(f"DESC CLASS: {s['PARAMS'].desc_class}\n")
        f.write(f"FEEDBACK PIPELINE: {feedback_pipeline_str(s['PARAMS'])}\n")
        f.write(f"GIVE PRED DESCRIPTIONS: {s['PARAMS'].give_pred_descriptions}\n")

        if err_msg != "":
            f.write("\nERROR MESSAGE ======================================\n\n")
            f.write(err_msg + "\n")
            return
        
        f.write("\nEXPERIMENT RESULTS ===================================\n\n")
        f.write(f"DOMAIN CHECK RUNS: {s['domain_check_runs']}\n")
        f.write(f"LANDMARK RUNS: {s['landmark_runs']}\n")
        f.write(f"VAL RUNS: {s['val_runs']}\n")
        f.write(f"HDE ITERATIONS: {s['hde_iterations']}\n")
        f.write(f"HDE TIMEOUT: {s['hde_timeout']}\n")
        f.write(f"ACTION TIMEOUT: {s['action_timeout']}\n")
        f.write(f"ACTION TIMEOUT CAUSE: {s['action_timeout_cause']}\n")
        f.write(f"EVALS PASSED: {s['evals_passed']}\n")
        f.write(f"TOTAL EVALS: {s['total_evals']}\n")
        f.write("LANGGRAPH PATH:\n\t" + '->\n\t'.join(s['langgraph_path']) + "\n")
        
        f.write("\nFINAL DOMAIN =====================================\n\n")
        try:
            domain_str = DomainParser()(s["json_last"].pddl_domain if s["json_last"] else "")
            f.write(str(domain_str))
        except Exception as e:
            f.write("No Domain was Generated by the Model, most likely because the pipeline never passed the domain construction stage.\n")

        f.write("\nMessages ===========================================\n\n\n")
        for msg in s["messages"]:
            f.write(msg.type.upper() + "\n\n")
            f.write(msg.content + "\n\n\n")
        

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
        logger.debug("Calling action model")
        json_obj = action_model.invoke(state["messages"])
        raw = json.dumps(json_obj.model_dump())
        return {
            "messages": [AIMessage(raw)],
            "json_last": json_obj,
            "langgraph_path": state["langgraph_path"] + ["call_action_model"]
        }

    def call_domain_model(state: State):
        try: 
            logger.debug("Calling domain model")
            json_obj = domain_model.invoke(state["messages"])
            raw = json.dumps(json_obj.model_dump())
        except Exception as e:
            # TODO: Fix
            msg = f"Error during feedback generation: {str(e)}" 
            logger.error(msg)
            raise RuntimeError(f"Failed to call domain model: {msg}")
        return {
            "messages": [AIMessage(raw)],
            "json_last": json_obj,
            "langgraph_path": state["langgraph_path"] + ["call_domain_model"]
        }

    def next_action(state: State):
        action_index = state["action_index"]
        actions_names = action_names(d, p)
        actions = state["actions"]
        if action_index >= len(actions_names):
            logger.debug(f"Done generating actions.")
            return {
                "actions_done": True,
                "actions" : actions + [state["json_last"]],
                "langgraph_path": state["langgraph_path"] + ["next_action"]
            }
        else:
            action_name = actions_names[action_index]
            logger.debug(
                "Starting Action %d/%d: %s",
                action_index + 1, len(actions_names), action_name
            )
            return {
                "messages": [action_message(d, p, action_name)],
                "action_index" : action_index + 1,
                "actions" : actions + [state["json_last"]],
                "action_iterations" : 0,
                "langgraph_path": state["langgraph_path"] + ["next_action"]
            }

    def check_action(state: State):
        res = check_action_output(state["json_last"])
        logger.debug(
            "Checking action... %s",
            "valid" if res is None else "invalid"
        )
        return {
            "messages": [res] if res else [],
            "action_valid" : res is None,
            "action_iterations" : state["action_iterations"] + 1,
            "langgraph_path": state["langgraph_path"] + ["check_action"]
        }

    def build_domain(state: State):
        logger.debug("Building domain from actions")
        full_domain_raw = domain_template(
            domain_name(d, p),
            state["actions"]
        )
        return {
            "messages" : [raw_domain_msg(full_domain_raw)],
            "json_last": DomainSchema(**{"pddl_domain":full_domain_raw}),
            "langgraph_path": state["langgraph_path"] + ["build_domain"]
        }

    def check_domain_syntax(state: State):
        try:
            res = check_domain_syntax_output(d, p, state["json_last"])
            logger.debug(
                "Checking domain syntax... %s",
                "valid" if res is None else "invalid"
            )
        except Exception as e:
            msg = f"Error during domain syntax check: {str(e)}"
            raise RuntimeError(msg)
        return {
            "messages": [res] if res else [],
            "domain_syntax_passed" : res is None,
            "hde_iterations" : state["hde_iterations"] + 1,
            "domain_check_runs" : state["domain_check_runs"] + (0 if res is None else 1),
            # "feedback_index": feedback_index,
            # "feedback_cycles": feedback_cycles,
            "langgraph_path": state["langgraph_path"] + ["check_domain_syntax"]
        }
    
    def feedback(state: State):
        landmark_feedback_msg : HumanMessage | None = None
        val_feedback_msg : HumanMessage | None = None
        try:
            if "landmark" in p.feedback_pipeline:
                landmark_feedback_msg = single_landmark_feedback(d, p, state["json_last"].pddl_domain)
                logger.debug(
                    "Checking landmarks... %s",
                    "passed" if landmark_feedback_msg is None else "failed"
                )
            if "validate" in p.feedback_pipeline:
                val_feedback_msg = single_val_feedback(d, p, state["json_last"].pddl_domain)
                logger.debug(
                    "Validating domain... %s",
                    "passed" if val_feedback_msg is None else "failed"
                )
        except Exception as e:
            # TODO: Fix
            msg = f"Error during feedback generation: {str(e)}" 
            logger.error(msg)
            landmark_feedback_msg = HumanMessage(msg)
            val_feedback_msg = HumanMessage(msg)
        return {
            "messages": [msg for msg in [landmark_feedback_msg, val_feedback_msg] if msg],
            "landmark_passed": landmark_feedback_msg is None, 
            "val_passed": val_feedback_msg is None,
            "landmark_runs": state["landmark_runs"] + (1 if landmark_feedback_msg is not None else 0),
            "val_runs": state["val_runs"] + (1 if val_feedback_msg is not None else 0),
            "langgraph_path": state["langgraph_path"] + ["feedback"]
        }
        
    def action_timeout_node(state: State):
        logger.debug("Action timeout reached, exiting.")
        actions_names = action_names(d, p)
        failed_action_name = actions_names[state["action_index"]]
        return {
            "action_timeout": True,
            "action_timeout_cause": failed_action_name,
            "langgraph_path": state["langgraph_path"] + ["action_timeout_node"]
        }
    
    def hde_timeout_node(state: State):
        logger.debug("HDE timeout reached.")
        return {
            "hde_timeout": True,
            "langgraph_path": state["langgraph_path"] + ["hde_timeout_node"]
        }
    
    def final_evaluation(state: State):
        res = val_evaluate(d, p, state["json_last"].pddl_domain)
        logger.debug(
            "Running evaluation of the domain. passed %d/%d",
            res[0], res[1]
        )
        return {
            "evals_passed": res[0],
            "total_evals": res[1],
            "langgraph_path": state["langgraph_path"] + ["final_evaluation"]
        }

    # Conditional Routing Helpers ==============================================

    def route_check_action(state: State) ->\
    Literal['action_timeout_node', 'next_action', 'call_action_model']:
        if state["action_iterations"] >= get_action_iteration_threshold():
            return "action_timeout_node"
        elif state["action_valid"]:
            return "next_action"
        else:
            return "call_action_model"

    def route_next_action(state: State) ->\
    Literal['build_domain', 'call_action_model']:
        if state["actions_done"]:
            return "build_domain"
        else:
            return "call_action_model"

    def route_check_domain_syntax(state: State) ->\
    Literal['hde_timeout_node', "feedback", 'call_domain_model']:
        if state["hde_iterations"] >= get_hde_iteration_threshold():
            return "hde_timeout_node"
        elif state["domain_syntax_passed"]:
            #return p.feedback_pipeline[state["feedback_index"] % len(p.feedback_pipeline)]
            return "feedback"
        else:
            return "call_domain_model"
    
    def route_feedback(state: State) ->\
    Literal['final_evaluation', 'call_domain_model']:
        if state["landmark_passed"] and state["val_passed"]:
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
    graph_builder.add_node("check_domain_syntax", check_domain_syntax)
    # graph_builder.add_node("landmark", landmark)
    # graph_builder.add_node("validate", validate)
    graph_builder.add_node("feedback", feedback)
    graph_builder.add_node("action_timeout_node", action_timeout_node)
    graph_builder.add_node("hde_timeout_node", hde_timeout_node)
    graph_builder.add_node("final_evaluation", final_evaluation)

    graph_builder.add_edge(START, "call_action_model")
    graph_builder.add_edge("call_action_model", "check_action")
    graph_builder.add_conditional_edges("check_action", route_check_action)
    graph_builder.add_conditional_edges("next_action", route_next_action)
    graph_builder.add_edge("build_domain", "check_domain_syntax")
    graph_builder.add_edge("call_domain_model", "check_domain_syntax")
    graph_builder.add_conditional_edges(
        "check_domain_syntax", 
        route_check_domain_syntax
    )
    # graph_builder.add_conditional_edges("landmark", route_landmark)
    # graph_builder.add_conditional_edges("validate", route_hde)
    graph_builder.add_conditional_edges("feedback", route_feedback)
    graph_builder.add_edge("action_timeout_node", END)
    graph_builder.add_edge("hde_timeout_node", "final_evaluation")
    graph_builder.add_edge("final_evaluation", END)

    return graph_builder.compile()

def graph_pipeline_image() -> None:
    """
    Saves the graph as a PNG image to the given filename.
    """
    experiment_init()
    graph = create_langgraph(None, Params()) # Dummy dataset and params
    graph.get_graph().draw_png("results/pipeline.png")

def run_experiment_instance(
    d: Dataset,     # Dataset
    p: Params,      # Experiment Parameters
    #results_lock,   # Lock on results file for thread safety
    batch_id : str,  # Identifier for the batch of experiments
    #results_path: str  # File to write results to
) -> tuple[bool, str, State]:
    """
    Executes a LangGraph for a single experiment, returns a bool indicating
    if the experiment ran without errors, and the final state of the experiment
    (in the event of an error, the final state before failure).
    """
    graph = create_langgraph(d, p)

    initial_state : State = {
        "run_id": batch_id,
        "PARAMS": p,
        "messages": init_msgs(d, p),
        "action_index": 0,
        "json_last": None,
        "action_valid": False,
        "actions_done": False,
        "actions" : [],
        "domain_syntax_passed": False,
        "val_passed": False,
        "feedback_index": 0,
        "feedback_cycles": 0,
        "landmark_passed": False,
        "landmark_runs": 0,
        "val_runs": 0,
        "domain_check_runs": 0,
        "action_iterations" : 0,
        "hde_iterations" : 0,
        "action_timeout" : False,
        "action_timeout_cause" : "",
        "hde_timeout" : False,
        "evals_passed": 0,
        "total_evals": 0,
        "langgraph_path": []
    }

    # Langgraph experiment state
    state : State = initial_state

    # Set the recursion limit for the graph execution to be high enough to 
    # accommodate the worst case scenario
    #TODO: occasionally seems to fail, investigate
    config = {
        "recursion_limit": 
            len(d.domains[p.domain_path].actions) * 
            get_action_iteration_threshold() + 
            get_hde_iteration_threshold() * 3 + 25,
    }

    # Run the graph
    try:
        logger.info("Running graph for %s", repr(p))
        for state in graph.stream(initial_state, stream_mode="values", config=config):
            continue
        return True, "", state
    except Exception as e: # pylint: disable=broad-except
        return False, f"Error: {type(e).__name__}, {e}", state

def run_experiment_instance_star(
    args: tuple[Dataset, Params, str]  # Dataset, Params, Batch ID
) -> tuple[bool, str, State]:
    """
    Wrapper for run_experiment to unpack the arguments.
    This is used for multiprocessing.
    """
    return run_experiment_instance(*args)

def experiment_init() -> None:
    load_dotenv()

    if not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY environment variable not set.\
                            Please set it in your .env file.")
    if not os.environ.get("DEEPSEEK_API_KEY"):
        raise RuntimeError("DEEPEEK_API_KEY environment variable not set.\
                            Please set it in your .env file.")

def run_experiment() -> None:
    """
    Driver, runs the experiments in parallel using the parameter grid
    """
    experiment_init()

    # Number of experiments we run in parallel, None means core count
    num_processes = THREADS if THREADS > 0 else None

    # Load the PDDL dataset
    dataset = Dataset()

    # Prepare the results output file and dir
    date_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    results_dir = os.path.join("results", date_time)
    os.makedirs(results_dir)
    results_path = os.path.join(results_dir, "results.csv")
    with open(results_path, 'w', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(RESULTS_HEADER)

    # Run the experiments in parallel and write the results
    args = [(dataset, params, date_time) for params in param_grid(dataset)]
    with mp.Pool(processes=num_processes) as pool:
        with open(results_path, 'a', encoding="utf-8") as res_file:
            csv_writer = csv.writer(res_file)
            for res in pool.imap_unordered(run_experiment_instance_star, args):
                (success, err_msg, state) = res
                write_message_log(state, err_msg, results_dir)
                if success:
                    csv_results_row = gen_csv_results(state)
                    csv_writer.writerow(csv_results_row)
                    
    print("Successfully joined all processes.")