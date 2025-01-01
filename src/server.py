import asyncio
import json

from threading import Thread
from flask import Flask, request, jsonify
from flask_cors import CORS
from websockets import serve

# Import your WebSocket server logic here
from session import Session
from response_logic import ResponseLogic

from db.utils import verify_password, hash_password
from db.queries import get_user_by_username, create_user
import re

class WebSocketServer:
    """
    WebSocket server for handling communication with users.
    """

    def __init__(self, config_file):
        """
        Initialize the WebSocket server.

        :param config_file (str): Path to the configuration file.
        """
        self.config = self._load_config(config_file)
        self.logic = ResponseLogic(self.config)


    def _load_config(self, config_file):
        """
        Load configuration file.

        :param config_file (str): Path to the configuration file.
        :returns (dict): Configuration data.
        :raises ValueError: If the configuration file cannot be loaded.
        """
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            raise ValueError(f"Error loading config: {e}")


    async def handle_client(self, websocket):
        """
        Handle WebSocket client connection.

        :param websocket (WebSocket): WebSocket connection object.
        """
        session = Session(websocket, self.logic)
        await session.handle_session()


    async def run(self):
        """
        Start WebSocket server.

        :raises Exception: If the server fails to start.
        """
        server = await serve(
            self.handle_client,
            self.config["host"],
            self.config["port"],
            ping_interval=60,
            ping_timeout=30,
        )
        print(f"WebSocket server started at ws://{self.config['host']}:{self.config['port']}")
        await server.wait_closed()


# Flask HTTP server
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})



@app.route("/register", methods=["POST"])
def register():
    """
    Handle user registration.

    :returns (Response): JSON response with a success message or an error.
    """
    data = request.json
    
    # Debugging - log received data
    print(data)
    
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    # Validate password strength
    if not is_valid_password(password):
        return jsonify({"error": (
            "Password must have at least 1 number, 1 special character, "
            "1 uppercase letter, 1 lowercase letter, and be at least 8 characters long."
        )}), 400

    try:
        # Hash the password
        password_hash = hash_password(password)
        
        # Create user in the database
        create_user(username, password_hash)

        print(f"User registered successfully: {username}")  # Debugging
        return jsonify({"message": "User registered successfully!"}), 201

    except Exception as e:
        print(f"Error during registration: {e}")
        return jsonify({"error": "Registration failed. Username might already exist."}), 400


def is_valid_password(password):
    """
    Validate the password strength.

    :param password: The password to validate.
    :return: True if the password meets the requirements, False otherwise.
    """
    if (
        len(password) >= 8 and
        re.search(r"[A-Z]", password) and  # At least one uppercase letter
        re.search(r"[a-z]", password) and  # At least one lowercase letter
        re.search(r"[0-9]", password) and  # At least one digit
        re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)  # At least one special character
    ):
        return True
    return False


@app.route("/login", methods=["POST"])
def login():
    """
    Handle user login.

    :returns (Response): JSON response with a success message and token or an error.
    """
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    try:
        user = get_user_by_username(username)
        if user is None or not verify_password(password, user["password_hash"]):
            return jsonify({"error": "Invalid username or password"}), 401

        return jsonify({"message": "Login successful!", "user_id": user["id"]}), 200

    except Exception as e:
        print(f"Error during login: {e}")
        return jsonify({"error": "An error occurred during login"}), 500


def run_flask():
    """
    Run the Flask HTTP server.
    """
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)


if __name__ == "__main__":
    # Start Flask server in a separate thread
    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    # Start WebSocket server
    try:
        websocket_server = WebSocketServer(config_file="../config.json")
        asyncio.run(websocket_server.run())
    except KeyboardInterrupt:
        print("\nServer terminated by user.")