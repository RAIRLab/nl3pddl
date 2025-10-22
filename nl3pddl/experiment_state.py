
# This file defines the master State object used by LangGraph
# the state object is updated at each node in the graph
# and passed to the next node.

from typing_extensions import TypedDict

from nl3pddl.dataset import Dataset
from nl3pddl.gen_prompts import init_msgs_tree

from .params import Params
from .response_schema import ActionSchema
from .search_tree import IndexedMessageTree

# LangGraph State, this object keeps track of all state for a single experiment
class State(TypedDict):
    """ The LangGraph application State"""
    #Run ID, identifier for the experiment run, allows us to filter in langsmith
    run_id: str
    # Experiment parameters, should not be modified during the run
    PARAMS: Params
    #LLM Message History up to the current tree level with associated scores
    messages: IndexedMessageTree
    # The json object of the message returned by the model
    #json_last: list[Any]
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

def gen_initial_state(batch_id: str, d: Dataset, p: Params) -> State:
    """ 
    Creates the initial state for the experiment.
    """
    return {
        "run_id": batch_id,
        "PARAMS": p,
        "messages": init_msgs_tree(d, p),
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