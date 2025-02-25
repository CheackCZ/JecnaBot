from .connection import get_connection


def create_user(username, password_hash):
    """
    Creates a new user and inserts him in the database.
    
    :param username (str): user's username.
    :param password_hash (str): user's password.
    """
    connection = get_connection()
    cursor = connection.cursor()
    
    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
            (username, password_hash),
        )
        connection.commit()
    finally:
        connection.close()


def get_user_by_username(username):
    """
    Fetch a user by username from the database.

    :param username: The username to search for.
    :return: A dictionary with user details or None if not found.
    """
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id, password_hash FROM users WHERE username = %s", (username,))
        return cursor.fetchone()
    finally:
        connection.close()