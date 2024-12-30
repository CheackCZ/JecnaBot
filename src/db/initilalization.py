import os
from .connection import get_connection


def initialize_database():
    """
    Initializes the database by executing the SQL script located in the same directory.

    The SQL script, "setup.sql", should contain all the necessary statements to set up the database schema and any initial data.

    :raises FileNotFoundError: If the "setup.sql" file is not found.
    :raises Exception: If there is an error during database initialization.
    """
    with open(os.path.join(os.path.dirname(__file__), "setup.sql"), "r") as file:
        sql_script = file.read()

    connection = get_connection()
    cursor = connection.cursor()
    try:
        for result in cursor.execute(sql_script, multi=True):
            pass
        print("Database initialized successfully.")
    except Exception as e:
        print(f"Error initializing database: {e}")
    finally:
        connection.close()

if __name__ == "__main__":
    initialize_database()