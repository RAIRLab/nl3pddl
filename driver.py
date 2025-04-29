import nl2pddl3 as n3p
import logging
import sqlite3

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    conn = n3p.reset_db("data/database.db")
    n3p.write_new_domains(conn)
    n3p.construct_initial_prompts(conn)
    # Print out the ModelRequest table

    # cursor = conn.cursor()
    # cursor.execute("SELECT * FROM ModelRequests")
    # rows = cursor.fetchall()
    # for row in rows:
    #     print(row)

    conn.close()