import bcrypt
import uuid


def hash_password(password):
    """
    Hashes a password using bcrypt.

    :param password (str): The password to be hashed.
    :returns (str): The hashed password as a string.
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password, hashed_password):
    """
    Verifies if the provided password matches the hashed password.

    :param password (str): The plain text password to verify.
    :param hashed_password (str): The hashed password to compare against.
    :returns (bool): True if the password matches the hashed password, False otherwise.
    """
    return bcrypt.checkpw(password.encode(), hashed_password.encode())