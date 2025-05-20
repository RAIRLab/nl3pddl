
import json
import logging
from typing import Any, Literal

import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph
from pydantic import BaseModel, Field

from typing import Annotated

from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages


import nl3pddl as n3p

load_dotenv()

if not os.environ.get("OPENAI_API_KEY"):
  raise RuntimeError("OPENAI_API_KEY environment variable not set. Please set it in your .env file.")


logging.getLogger().setLevel(logging.INFO)

dataset = n3p.Dataset()

class ActionSchema(BaseModel):
    """Always use this tool to structure your response to the user."""
    pddl_action: str = Field(description="String of raw typed STRIPS PDDL code for a single action (:action name :parameters (...) :precondition (...) :effect (...))")
    predicates: list[str] = Field(description="List of allowed predicates of the form (name arg1 - type1 arg2 - type2 ...) from this action and previous actions, adding any new predicates used in this action")
    types: list[str] = Field(description="List of allowed types from this action and previous actions, adding any new types used in this action")

class DomainSchema(BaseModel):
    """Always use this tool to structure your response to the user."""
    pddl_domain: str = Field(description="String of raw typed STRIPS PDDL code for an entire domain (:domain name :requirements (...) :types (...) :predicates (...) :functions (...) :action (...))")

class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]
    # The index of the action we are currently trying to write

    # The json object of the message returned by the model
    json_last: Any  

    action_index: int
    # The current action has passed validation
    action_valid: bool
    # We are done and have constructed all actions
    actions_done: bool
    # List of good action outputs
    actions : list[Any]

    # The domain we are currently working on is syntactically valid
    domain_syn_val: bool

    # The domain we are currently working on is HDE
    domain_hde_val: bool
    hde_iterations : int
    

for p in n3p.param_grid(dataset):
    model = init_chat_model(p.model, model_provider=p.provider)
    action_model = model.with_structured_output(ActionSchema)
    domain_model = model.with_structured_output(DomainSchema)

    # Lang-graph nodes =======================================================

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
        actions_names = n3p.action_names(dataset, p)
        actions = state["actions"]
        if action_index >= len(actions_names):
            return {
                "actions_done": True,
                "actions" : actions + [state["json_last"]]
            }
        else:
            action_name = actions_names[action_index]
            return {
                "messages": [n3p.action_message(dataset, p, action_name)],
                "action_index" : action_index + 1,
                "actions" : actions + [state["json_last"]]
            }
    
    def check_action(state: State):
        res = n3p.check_action_output(n3p.domain_name(dataset, p), p, state["json_last"])
        return {
            "messages": [res] if res else [],
            "action_valid" : res is None
        }

    def build_domain(state: State):
        full_domain_raw = n3p.domain_template(n3p.domain_name(dataset, p), state["actions"])
        return {
            "messages" : [HumanMessage(full_domain_raw)],
            "json_last": DomainSchema(**{"pddl_domain":full_domain_raw})
        }

    def check_domain(state: State):
        res = n3p.check_domain_output(p, state["json_last"])
        return {
            "messages": [res] if res else [],
            "domain_syn_val" : res is None
        }

    def validate(state: State):
        res = n3p.val_all(dataset, p, state["json_last"].pddl_domain)
        return {
            "messages": [res] if res else [],
            "domain_hde_val" : res is None
        }
    
    # Conditional Routing Helpers =============================================
    # TODO: Move these to the nicer inline notation

    def route_actions(state: State) -> Literal['next_action', 'call_action_model']:
        if state["action_valid"]:
            return "next_action"
        else:
            return "call_action_model"
        
    def route_actions_done(state: State) -> Literal['build_domain', 'call_action_model']:
        if state["actions_done"]:
            return "build_domain"
        else:
            return "call_action_model"
    
    def route_domain_syn(state: State) -> Literal['validate', 'call_domain_model']:
        if state["domain_syn_val"]:
            return "validate"
        else:
            return "call_domain_model"
        
    def route_hde(state: State) -> Literal['call_domain_model', '__end__']:
        if state["domain_hde_val"]:
            return "call_domain_model"
        else:
            return END
    
    # Create the graph
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

    graph = graph_builder.compile()

    # Save the graph to a png file
    graph.get_graph().draw_png(f"graph.png")

    initial_state = {
        "messages": n3p.init_msgs(dataset, p),
        "action_index": 0,
        "json_last": None,
        "action_valid": False,
        "actions_done": False,
        "actions" : [],
        "domain_syn_val": False,
        "domain_hde_val": False,
        "hde_iterations" : 0
    }
    
    for step in graph.stream(initial_state, stream_mode="values", debug=True):
        step["messages"][-1].pretty_print()

        
        
        



