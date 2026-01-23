from flask_socketio import emit
from backend.extensions import socketio
from backend.utils import Logger

logger = Logger.get_logger("JuFireX_Socket")

@socketio.on("connect")
def handle_connect():
    logger.info("Client connected")
    emit("message", {"data": "Connected to JuFireX Backend"})

@socketio.on("disconnect")
def handle_disconnect():
    logger.info("Client disconnected")

@socketio.on("ping")
def handle_ping():
    emit("pong")
