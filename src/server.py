import asyncio
import json

from threading import Thread
from flask import Flask, request, jsonify
from flask_cors import CORS
from websockets import serve

# Import your WebSocket server logic here
from session import Session
from response_logic import ResponseLogic

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
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    # Add user registration logic here (e.g., save to the database)
    print(f"Registered user: {username}")  # Debugging
    return jsonify({"message": "User registered successfully!"}), 201


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

    # Add user login logic here (e.g., verify credentials)
    print(f"Login attempt for user: {username}")  # Debugging
    return jsonify({"message": "Login successful!", "token": "sample-token"}), 200


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