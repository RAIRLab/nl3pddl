
import os
import sqlite3
import logging
import json

BASE_PROMPT_PATH = "data/prompts/start_prompt.txt"
CONTEXT_PATH = "data/context"
CONTEXT1 = "blocksworld"
CONTEXT2 = "logistics"

MODELS = [
    "gpt-4.1",
    "gpt-4.1-mini",
    "gpt-4.1-nano",
    "o1-mini",
    "o3-mini",
    "gpt-4o-mini",
]


def append_context_example(input_messages : list[dict[str, str]], context_id : str) -> None:
    """Adds the context example to the input chat completion messages list"""
    context_template_path = os.path.join(CONTEXT_PATH, f"{context_id}.pddl.txt")
    context_nl_path = os.path.join(CONTEXT_PATH, f"{context_id}.txt")
    context_output_path = os.path.join(CONTEXT_PATH, f"{context_id}.pddl")
    with open(context_template_path, "r") as f:
        context_template_str = f.read()
    with open(context_nl_path, "r") as f:
        context_nl_str = f.read()
    with open(context_output_path, "r") as f:
        context_output_str = f.read()
    input_messages.append(
        {"role" : "user", "content": context_nl_str + "\n" + context_template_str}
    )
    input_messages.append(
        {"role" : "assistant", "content": context_output_str}
    )


def chat_completion_prompt(new_template:str) -> list[dict[str, str]]:
    messages = []
    with open(BASE_PROMPT_PATH, "r") as f:
        base_prompt_str = f.read()
    messages.append(
        {"role" : "system", "content": base_prompt_str}
    )
    append_context_example(messages, CONTEXT1)
    append_context_example(messages, CONTEXT2)
    messages.append(
        {"role" : "user", "content": new_template}
    )
    return messages


def construct_initial_prompts(conn : sqlite3.Connection) -> None:
    """Constructs the initial prompts for all the domains in the database"""
    cur = conn.cursor()
    for model in MODELS:
        rows = cur.execute("""
            SELECT dt.raw_text, d.id, d.label 
            FROM Domains d
            JOIN DomainTemplateOwners dto ON dto.domain_id = d.id
            JOIN DomainTemplates dt ON dto.template_id = dt.id
        """).fetchall()
        for (template_raw_text, domain_id, domain_name) in rows:
            logging.info(f"Constructing initial prompt for {domain_name} with model {model}")
            messages = chat_completion_prompt(template_raw_text)
            cur.execute(
                "INSERT INTO ModelRequests (loop_id, model_name, api_provider, raw_json) VALUES (?, ?, ?, ?)",
                (0, model, "openai", json.dumps(messages))
            )
            request_id = cur.lastrowid
            cur.execute(
                "INSERT INTO ModelRequestOwners (domain_id, owner_id, request_id) VALUES (?, ?, ?)",
                (domain_id, None, request_id)
            )
    try:
        conn.commit()
    except:
        logging.error(f"Error committing changes to the database")
        conn.rollback()

def construct_reprompts(conn : sqlite3.Connection) -> None:
    raise NotImplementedError("Not implemented yet")