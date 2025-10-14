"""
This file contains the driver for the NL3PDDL project.
"""

# Standard library imports
import os
import csv
import json
from typing import Any, Literal
import multiprocessing as mp
from datetime import datetime

# External package imports

from dotenv import load_dotenv

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph

from .config import THREADS
from .check_output import check_action_output, check_domain_syntax_output
from .gen_prompts import action_message, domain_template, init_msgs, raw_domain_msg
from .dataset import Dataset
from .params import Params, action_names, domain_name, get_action_iteration_threshold, get_hde_iteration_threshold, param_grid
from .feedback_eval import multi_landmark_feedback, multi_val_feedback, val_evaluate, val_feedback_test
from .logger import logger, gen_csv_results, RESULTS_HEADER, write_message_log
from .response_schema import ActionSchema, DomainSchema
from .search_tree import IndexedMessageTree
from .experiment_state import State        

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
        json_obj = action_model.invoke(state["messages"].history())
        raw = json.dumps(json_obj.model_dump())
        return {
            "messages": state["messages"].insert_on_current_branch_json(AIMessage(raw), json_obj),
            "langgraph_path": state["langgraph_path"] + ["call_action_model"]
        }
    
    def call_domain_model(state: State):
        json_obj = domain_model.invoke(state["messages"].history())
        raw = json.dumps(json_obj.model_dump())
        return {
            "messages": state["messages"].insert_on_current_branch_json(AIMessage(raw), json_obj),
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
                "actions" : actions + [state["messages"].json_last()],
                "langgraph_path": state["langgraph_path"] + ["next_action"]
            }
        else:
            action_name = actions_names[action_index]
            logger.debug(
                "Starting Action %d/%d: %s",
                action_index + 1, len(actions_names), action_name
            )
            updated_messages = state["messages"].insert_on_current_branch(action_message(d, p, action_name))
            return {
                "messages": updated_messages,
                "action_index" : action_index + 1,
                "actions" : actions + [state["messages"].json_last()],
                "action_iterations" : 0,
                "langgraph_path": state["langgraph_path"] + ["next_action"]
            }

    def check_action(state: State):
        if state["messages"].json_last() is None:
            raise ValueError("No action to check")
        res = check_action_output(state["messages"].json_last())
        logger.debug(
            "Checking action... %s",
            "valid" if res is None else "invalid"
        )
        return {
            "messages": state["messages"].insert_on_current_branch(res) if res else state["messages"],
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
            "messages" : state["messages"].insert_on_current_branch_json(raw_domain_msg(full_domain_raw), {"pddl_domain":full_domain_raw}),
            "langgraph_path": state["langgraph_path"] + ["build_domain"]
        }
    
    def check_domain_syntax(state: State):
        json_last = state["messages"].json_last()
        res = check_domain_syntax_output(d, p, json_last)
        new_messages = state["messages"].insert_on_current_branch(res) if res else state["messages"]
        #If syntactically valid, immediatly update the score based on how well it does on the evals
        if res is None:
            try:
                scores = val_feedback_test(d, p, json_last["pddl_domain"])
                new_messages.get().score = scores[0]
            except Exception as e:
                new_messages.get().score = 0
        return {
            # TODO: need to actually append the last message to proposed if the syntax check failed
            "messages": new_messages,
            # We pass the syntax check if any of the proposed messages passed it
            "domain_syntax_passed" : res is None,
            "hde_iterations" : state["hde_iterations"] + 1,
            "domain_check_runs" : state["domain_check_runs"] + (0 if res is None else 1),
            "langgraph_path": state["langgraph_path"] + ["check_domain_syntax"]
        }

    def feedback(state: State):
        landmark_feedback_msgs : list[HumanMessage] = []
        val_feedback_msgs : list[HumanMessage] = []
        current_node = state["messages"].get()
        
        # Exit early if we have a perfect score
        # TODO: Extract 10 as the constant for perfect score
        if current_node.score == 10:
            return {
                "landmark_passed": True,
                "val_passed": True,
                "langgraph_path": state["langgraph_path"] + ["feedback"]
            }

        try:
            if "landmark" in p.feedback_pipeline:
                landmark_feedback_msgs = multi_landmark_feedback(d, p, state["messages"].json_last()["pddl_domain"])
            if "validate" in p.feedback_pipeline:
                val_feedback_msgs = multi_val_feedback(d, p, state["messages"].json_last()["pddl_domain"])
        except Exception as e:
            # TODO: Fix
            msg = f"Error during feedback generation: {str(e)}" 
            logger.error(msg)
            val_feedback_msgs = [HumanMessage(msg)]

        state["messages"].insert_batch_on_current_branch(landmark_feedback_msgs + val_feedback_msgs)
        state["messages"].select_best_branch()
        
        return {
            "messages": state["messages"],
            "landmark_passed": landmark_feedback_msgs is None,
            "val_passed": val_feedback_msgs is None,
            "landmark_runs": state["landmark_runs"] + (1 if landmark_feedback_msgs is not None else 0),
            "val_runs": state["val_runs"] + (1 if val_feedback_msgs is not None else 0),
            "langgraph_path": state["langgraph_path"] + ["feedback"]
        }
        
    def action_timeout_node(state: State):
        logger.debug("Action timeout reached, exiting.")
        actions_names = action_names(d, p)
        action_index = state["action_index"] - 1
        failed_action_name = actions_names[action_index]
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
        res = val_evaluate(d, p, state["messages"].json_last()["pddl_domain"])
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

def init_messages_as_message_tree(d: Dataset, p: Params) -> IndexedMessageTree:
    """
    Initializes the message history as an IndexedMessageTree.
    """
    msgs = init_msgs(d, p)
    tree = IndexedMessageTree()
    for msg in msgs:
        tree.insert_on_current_branch(msg)
    return tree

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
        "messages": init_messages_as_message_tree(d, p),
        "action_index": 0,
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