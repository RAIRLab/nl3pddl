
"""
This file defines the response schema for the LLM to output,
LLMs will be forced to output in these json formats.
WARNING: Comments are used by the LLM! Change them with care.
"""

from pydantic import BaseModel, Field

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
