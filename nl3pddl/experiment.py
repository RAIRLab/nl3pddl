"""
This file contains the driver for the NL3PDDL project.
"""

# Standard library imports
import os
import csv
import json
import random
from typing import Literal
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import time

# External package imports
from dotenv import load_dotenv
import tiktoken
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph

from langchain.globals import set_verbose
set_verbose(True)

from .config import (
    THREADS,
    ACTION_THRESHOLD,
    HDE_THRESHOLD,
    PRICE,
    SKIP_EXPERIMENT,
    AVERAGE_INPUT_TOKENS,
    AVERAGE_OUTPUT_TOKENS,
    AVERAGE_CALLS_PER_EXPERIMENT,
)
from .check_output import check_action_output, check_domain_syntax_output
from .gen_prompts import action_message, domain_template, raw_domain_msg
from .dataset import Dataset
from .params import Params, action_names, domain_name, param_grid
from .feedback_eval import multi_landmark_feedback, multi_val_feedback, val_evaluate, val_feedback_test
from .logger import logger
from .response_schema import ActionSchema, DomainSchema
from .experiment_state import State, gen_initial_state        
from .experiment_reporter import gen_csv_results, RESULTS_HEADER, write_message_log

# Experiments Helpers ==========================================================

def create_langgraph(d: Dataset, p: Params) -> CompiledStateGraph:
    """
    Creates a langgraph for a single experiment with the given
    experimental parameters.
    """
    # Handle Hugging Face models through OpenAI-compatible API
    # https://huggingface.co/NousResearch/Hermes-4-405B?inference_api=true&inference_provider=nebius&language=python&client=openai
    if p.provider == "huggingface":
        model = init_chat_model(
            p.model,
            model_provider="openai",
            timeout=60,
            max_retries=3,
            base_url="https://router.huggingface.co/v1",
            api_key=hf_token,
        )
    else:
        model = init_chat_model(p.model, model_provider=p.provider, timeout=60, max_retries=3)

    action_model = model.with_structured_output(ActionSchema)
    domain_model = model.with_structured_output(DomainSchema)

    # Lang-graph nodes =========================================================

    def call_action_model(state: State):
        """ 
        Calls the model using the ActionSchema structured output to generate the next action. 
        """
        logger.debug("Calling action model")
        history = state["messages"].squashed_message_history()
        json_obj = action_model.invoke(history)
        raw = json.dumps(json_obj.model_dump())
        return {
            "messages": state["messages"].insert_on_current_branch_json(
                AIMessage(raw),
                json_obj, 
                "call_action_model"
            ),
            "langgraph_path": state["langgraph_path"] + ["call_action_model"]
        }
    
    def call_domain_model(state: State):
        """
        Calls the model using the DomainSchema structured output to generate the domain.
        """
        history = state["messages"].squashed_message_history()
        json_obj = domain_model.invoke(history)
        raw = json.dumps(json_obj.model_dump())
        return {
            "messages": state["messages"].insert_on_current_branch_json(
                AIMessage(raw),
                json_obj, 
                "call_domain_model"
            ),
            "langgraph_path": state["langgraph_path"] + ["call_domain_model"]
        }

    def next_action(state: State):
        """
        Stores the current action and prepares for the next action generation.
        """
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
            updated_messages = state["messages"].insert_on_current_branch(
                action_message(d, p, action_name),
                "next_action"
            )
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
        updated_messages = state["messages"].insert_on_current_branch(
            res, 
            "check_action"
        ) if res else state["messages"]
        return {
            "messages": updated_messages,
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
        updated_messages = state["messages"].insert_on_current_branch_json(
            raw_domain_msg(full_domain_raw), 
            {"pddl_domain":full_domain_raw}, 
            "build_domain"
        )
        #updated_messages.get().update_score(float("inf"), 0) # Search starts here!
        return {
            "messages" : updated_messages,
            "langgraph_path": state["langgraph_path"] + ["build_domain"]
        }
    
    def check_domain_syntax(state: State):
        json_last = state["messages"].json_last()
        res = check_domain_syntax_output(d, p, json_last)
        # Only add a new message if we found an error
        new_messages = state["messages"].insert_on_current_branch(
            res, "check_domain_syntax"
        ) if res is not None else state["messages"]
        #If syntactically valid, immediatly update the score based on how well it does on the evals, note that lower is better!
        if res is None:
            try:
                scores = val_feedback_test(d, p, json_last["pddl_domain"])
                new_messages.update_score(scores[1] - scores[0])
            except Exception as e:
                # If validation fails, use a penalty score (no passing tests)
                logger.error(f"Error during validation test: {e}")
                # TODO: shouldn't hardcode the error penalty like this
                new_messages.update_score(float("inf"))
        return {
            "messages": new_messages,
            # We pass the syntax check if any of the proposed messages passed it
            "domain_syntax_passed" : res is None,
            "hde_iterations" : state["hde_iterations"] + 1,
            "domain_check_runs" : state["domain_check_runs"] + (0 if res is None else 1),
            "langgraph_path": state["langgraph_path"] + ["check_domain_syntax"]
        }

    def feedback(state: State):
        landmark_feedback_msgs : list[HumanMessage] | None = []
        val_feedback_msgs : list[HumanMessage] | None = []
        feedback_messages : list[HumanMessage] | None = []
        current_node = state["messages"].get()
        
        # Stop giving feedback if H score is 0 (perfect) or no feedback pipeline
        if current_node.h == 0 or p.feedback_pipeline == []:
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

            if landmark_feedback_msgs is not None and val_feedback_msgs is not None:
                feedback_messages = landmark_feedback_msgs + val_feedback_msgs

            # If "random-single" is in the pipeline, select a single random feedback message from the combined feedback and just use that
            if "random-single" in p.feedback_pipeline and feedback_messages is not None and len(feedback_messages) > 0:
                feedback_messages = [random.choice(feedback_messages)]

        except Exception as e:
            msg = f"Error during feedback generation: {str(e)}" 
            logger.error(msg)
            val_feedback_msgs = [HumanMessage(msg)]

        state["messages"].insert_batch_on_current_branch(
            feedback_messages, langraph_node="feedback"
        )
        state["messages"] = state["messages"].select_best_branch()
        
        return {
            "messages": state["messages"],
            "landmark_passed": landmark_feedback_msgs is None,
            "val_passed": val_feedback_msgs is None,
            # TODO: not used anymore
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
        if state["action_iterations"] >= ACTION_THRESHOLD:
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
        if state["hde_iterations"] >= HDE_THRESHOLD:
            return "hde_timeout_node"
        elif state["domain_syntax_passed"]:
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
    graph_builder.add_conditional_edges("feedback", route_feedback)
    graph_builder.add_edge("action_timeout_node", END)
    graph_builder.add_edge("hde_timeout_node", "final_evaluation")
    graph_builder.add_edge("final_evaluation", END)

    return graph_builder.compile()

def graph_pipeline_image() -> None:
    """
    Saves the graph as a PNG image.
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

    initial_state : State = gen_initial_state(batch_id, d, p)

    # Langgraph experiment state
    state : State = initial_state

    if SKIP_EXPERIMENT:
        logger.info(f"Skipping experiment {batch_id} for domain {p.domain_path} with path {p.feedback_pipeline} as per configuration.")
        return True, "Experiment skipped", state

    graph = create_langgraph(d, p)

    # TODO: this is no longer meaningful in light of search
    config = {
        "recursion_limit": 
            len(d.domains[p.domain_path].actions) * 
            ACTION_THRESHOLD + 
            HDE_THRESHOLD * 3 + 25,
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
        raise RuntimeError("DEEPSEEK_API_KEY environment variable not set.\
                            Please set it in your .env file.")

    if not os.environ.get("HF_API_KEY"):
        raise RuntimeError("HF_API_KEY environment variable is not set.\
                            Please set it in your .env file.")
    else:
        global hf_token 
        hf_token = os.environ.get("HF_API_KEY")

def experiment_cost_estimate_prompt(param_list) -> None:
    num_experiments = len(param_list)
    per_experiment_call_costs = []

    # Warn about missing price entries 
    models = set(p.model for p in param_list)
    for model in models:
        if model not in PRICE:
            print(f"Price information for model '{model}' not found. Cost estimation may be inaccurate.")

    # Sum up per-experiment costs
    for p in param_list:
        if p.model not in PRICE:
            continue
        price_entry = PRICE[p.model]
        in_rate = float(price_entry["input"])  # USD per input token
        out_rate = float(price_entry["output"])  # USD per output token
        call_cost = in_rate * float(AVERAGE_INPUT_TOKENS) + out_rate * float(AVERAGE_OUTPUT_TOKENS)
        per_experiment_call_costs.append(call_cost)

    estimated_total_cost = float(AVERAGE_CALLS_PER_EXPERIMENT) * sum(per_experiment_call_costs)

    print(f"Experiments (param grid size): {num_experiments}")
    print(f"Avg calls/experiment: {AVERAGE_CALLS_PER_EXPERIMENT}")
    print(f"Avg tokens per call: in={AVERAGE_INPUT_TOKENS}, out={AVERAGE_OUTPUT_TOKENS}")
    print(f"Estimated total cost (USD): ${estimated_total_cost:,.2f}")

    choice = input("Proceed with experiment? [y/N]: ").strip().lower()
    if choice != "y":
        print("Aborting by user choice.")
        exit(1)

def run_experiment() -> None:
    """
    Driver, runs the experiments in parallel using the parameter grid
    """
    experiment_init()

    # Load the PDDL dataset
    dataset = Dataset()

    # Build full parameter list to size the run and estimate cost
    param_list = list(param_grid(dataset))
    
    # Estimate cost and confirm with user before starting the experiment
    experiment_cost_estimate_prompt(param_list)

    # Prepare the results output file and dir
    date_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    results_dir = os.path.join("results", date_time)
    os.makedirs(results_dir)
    results_path = os.path.join(results_dir, "results.csv")
    with open(results_path, 'w', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(RESULTS_HEADER)

    # Run the experiments in parallel and write the results
    args = [(dataset, params, date_time) for params in param_list]
    num_processes = THREADS if THREADS > 0 else len(args)

    print("number of processes", num_processes)
    time.sleep(1)

    with ThreadPoolExecutor(max_workers=num_processes) as pool:
        with open(results_path, 'a', encoding="utf-8") as res_file:
            csv_writer = csv.writer(res_file)
            for res in pool.map(run_experiment_instance_star, args):
                try:
                    (success, err_msg, state) = res
                    write_message_log(state, err_msg, results_dir)
                    if success:
                        csv_results_row = gen_csv_results(state)
                        csv_writer.writerow(csv_results_row)
                except Exception as e:
                    logger.error("Error processing result: %s", e)

    print("Successfully joined all threads. Experiment complete.")
