
import os 
import sqlite3
import logging
import json

from openai import OpenAI

client = OpenAI()

def get_responses(conn: sqlite3.Connection, loop_id : int) -> None:
    """
    Loop through all available requests at a given loop_id and get the responses from the OpenAI API.
    """
    cursor = conn.cursor()
    requests = cursor.execute("""
        SELECT * FROM ModelRequests WHERE loop_id = ?
    """, (loop_id,)).fetchall()
    for (request_id, loop_id, model_name, api_provider, raw_json) in requests:
        logging.info(f"Getting response for request {request_id} with model {model_name}")
        messages = json.loads(raw_json)
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=messages
            )
            response_str = response.choices[0].message.content
            cursor.execute(
                "INSERT INTO ModelResponses (loop_id, error, raw_response) VALUES (?, ?, ?)",
                (loop_id, False, response_str)
            )
        except Exception as e:
            logging.error(f"Error getting response for request {request_id} with model {model_name}: {e}")
            cursor.execute(
                "INSERT INTO ModelResponses (loop_id, error, raw_response) VALUES (?, ?, ?)",
                (loop_id, True, response_str)
            )
        finally:
            response_id = cursor.lastrowid
            cursor.execute(
                "INSERT INTO ModelResponseOwners (request_id, response_id) VALUES (?, ?)",
                (request_id, response_id)
            )
            conn.commit()
        