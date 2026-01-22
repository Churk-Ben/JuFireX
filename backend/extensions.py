from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO

db = SQLAlchemy()
socketio = SocketIO(cors_allowed_origins="*", logger=True, engineio_logger=True, ping_timeout=60, ping_interval=25)
