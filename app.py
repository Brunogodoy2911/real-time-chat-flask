from flask import Flask, jsonify, request, render_template, current_app
from repository.database import db
from datetime import datetime
from db_models.message import Message
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SECRET_KEY"] = "SECRET_KEY_WEBSOCKET"

db.init_app(app)
socketio = SocketIO(app)

@app.route("/api/send_message", methods=["POST"])
def send_message():
    data = request.get_json()

    if "content" not in data:
        return jsonify({"error": "Content is required"}), 400
    
    timestamp = datetime.now()

    new_message = Message(content=data["content"], timestamp=timestamp)

    db.session.add(new_message)
    db.session.commit()

    return jsonify({"message": "The message was sent successfully", "data": new_message.to_dict()}), 201

@app.route("/api/messages", methods=["GET"])
def get_messages():
    messages = Message.query.order_by(Message.timestamp.desc()).all()
    messages_list = [message.to_dict() for message in messages]
    
    return jsonify(messages_list), 200

@app.route("/", methods=["GET"])
def index():
   
    return render_template("index.html")

@socketio.on("message")
def handle_message(data):

    if "content" not in data:
        emit("error", {"message": "Content is required"}, room=request.sid)
        return False
    
    content = data["content"]
    timestamp = datetime.now()

    new_message = Message(content=content, timestamp=timestamp)

    with current_app.app_context():
        db.session.add(new_message)
        db.session.commit()

        message_data = new_message.to_dict()
    
    emit("new_message", message_data, broadcast=True)
    
if __name__ == "__main__":
    app.run(debug=True)