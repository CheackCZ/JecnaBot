import mysql.connector
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

def get_connection():
    """
    Returns the connection data for database.
    
    Returns: mysql.connector.connect: database connection data (Host, Database User, Database Password and Database Name) 
    """
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
