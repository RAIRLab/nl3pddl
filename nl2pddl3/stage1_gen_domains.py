
import time
import os
import sqlite3
import json
import logging
import pickle
from typing import Dict
from pddl.core import Domain
from pddl.parser.domain import DomainParser

DB_FILE_PATH = "data/domains.db"
CONFIG_FILE_PATH = "data/config.json"
TEMPLATE_FILE_NAME = "template.pddl.txt"
GROUND_TRUTH_FILE_NAME = "ground.pddl"
NL_FILE_NAME = "nl.txt"


def get_new_domains() -> list[str]:
    """returns a list of paths of folders in data/domains marked as new in data/config.json"""
    with open(CONFIG_FILE_PATH, "r") as f:
        config = json.load(f)
    new_domains = []
    for domain in config["new_domains"]:
        domain_path = os.path.join("data/domains", domain)
        if os.path.isdir(domain_path):
            new_domains.append(domain_path)
        else:
            logging.warning(f"Domain path {domain_path} is listed as a new domain in data/config.json but does not exist.")
    return new_domains

class DomainIds:
    domain_id: int
    predicate_id_map: Dict[str, int]
    action_id_map: Dict[str, int]

    def __init__(self, domain_id, predicate_id_map, action_id_map):
        self.domain_id = domain_id
        self.predicate_id_map = predicate_id_map
        self.action_id_map = action_id_map

def write_domain_raw(conn: sqlite3.Connection, domain_str: str, domain_obj: Domain=None, loop_num: int=0 ) -> DomainIds:
    """ 
    Writes a raw domain string into the database domain table, and adds associated predicates and actions to the database.
    Returns relevant IDs for created objects
    """
    cursor = conn.cursor()
    created_at = time.time()
    if domain_obj is None and loop_num > 0:
        domain_obj = DomainParser()(domain_str)
        logging.warning(f"Creating blob in write_domain, this is probably an error!")
    label = domain_obj.name
    blob : bytes = pickle.dumps(domain_obj)
    # Write the domain itself into the database
    cursor.execute(
        "INSERT INTO Domains (created_at, loop_number, raw_pddl, raw_blob) VALUES (?, ?, ?, ?)",
        (created_at, loop_num, label, domain_str, blob)
    )
    domain_id = cursor.lastrowid

    # Write domain predicates into the database
    pred_map = {}
    for predicate in domain_obj.predicates:
        cursor.execute(
            "INSERT INTO Predicates (predicate) VALUES (?)",
            (predicate.name)
        )
        predicate_id = cursor.lastrowid
        cursor.execute(
            "INSERT INTO PredicateOwners (domain_id, predicate_id) VALUES (?, ?)",
            (domain_id, predicate_id)
        )
        pred_map[predicate.name] = predicate_id
    
    # Write domain actions into the database
    action_id_map = {}
    for action in domain_obj.actions:
        cursor.execute(
            "INSERT INTO Actions (action) VALUES (?)",
            (action.name)
        )
        action_id = cursor.lastrowid
        cursor.execute(
            "INSERT INTO ActionOwners (domain_id, action_id) VALUES (?, ?)",
            (domain_id, action_id)
        )
        action_id_map[action.name] = action_id
    return DomainIds(domain_id, pred_map, action_id_map)

def write_domain(conn: sqlite3.Connection, domain_dir_path: str) -> None:
    """Takes a domain directory path, parses all the data into the database"""

    # Write the ground truth domain into the database
    domain_path = os.path.join(domain_dir_path, GROUND_TRUTH_FILE_NAME)
    with open(domain_path, "r") as f:
        domain_str = f.read()
    domain_obj = DomainParser()(domain_str)
    ids = write_domain_raw(conn, domain_str, domain_obj)

    # Write the domain template domain into the database
    template_path = os.path.join(domain_dir_path, TEMPLATE_FILE_NAME)
    with open(template_path, "r") as f:
        template_str = f.read()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO DomainTemplates (raw_pddl) VALUES (?)",
        (template_str)
    )
    template_id = cursor.lastrowid
    cursor.execute(
        "INSERT INTO DomainTemplateOwners (domain_id, template_id) VALUES (?, ?)",
        (ids.domain_id, template_id)
    )

    # Write the descriptions of the domain, predicates and actions into the database
    nl_path = os.path.join(domain_dir_path, NL_FILE_NAME)
    with open(nl_path, "r") as f:
        nl_str = f.read()
    nl_json = json.loads(nl_str)
    for (desc_class, desc) in nl_json["overall"]:
        cursor.execute("INSERT INTO Descriptions (nl, nl_class) VALUES (?)", (desc, desc_class))
        description_id = cursor.lastrowid
        cursor.execute(
            "INSERT INTO DomainDescriptionOwners (domain_id, description_id) VALUES (?, ?)",
            (ids.domain_id, description_id)
        )

    assert len(nl_json["predicates"]) == len(ids.predicate_id_map), "Predicate count mismatch"
    for (pred_name, pred_obj) in nl_json["predicates"]:
        for (desc_class, desc) in pred_obj["overall"]:
            cursor.execute("INSERT INTO Descriptions (nl, nl_class) VALUES (?, ?)", (desc, desc_class))
            description_id = cursor.lastrowid
            cursor.execute(
                "INSERT INTO PredicateDescriptionOwners (predicate_id, description_id) VALUES (?, ?)",
                (ids.predicate_id_map[pred_name], description_id)
            )
        
    assert len(nl_json["actions"]) == len(ids.action_id_map), "Action count mismatch"
    for (action_name, action_obj) in nl_json["actions"]:
        for (desc_class, desc) in action_obj["overall"]:
            cursor.execute("INSERT INTO Descriptions (nl, nl_class) VALUES (?, ?)", (desc, desc_class))
            description_id = cursor.lastrowid
            cursor.execute(
                "INSERT INTO ActionDescriptionOwners (action_id, description_id) VALUES (?, ?)",
                (ids.action_id_map[action_name], description_id)
            )

def write_new_domains(conn: sqlite3.Connection) -> None:
    """Adds all new domains to the database"""
    new_domains = get_new_domains()
    for domain_path in new_domains:
        write_domain(conn, domain_path)
        logging.info(f"Added domain {domain_path} to the database.")
    conn.commit()
    logging.info("All new domains added to the database.")
    