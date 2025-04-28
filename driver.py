import nl2pddl3 as n3p
import logging

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    conn = n3p.reset_db("data/database.db")
    n3p.write_new_domains(conn)
    conn.close()