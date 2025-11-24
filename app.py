import os
from flask import Flask, jsonify, request, render_template, current_app, redirect, url_for
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
import bcrypt
from repository.database import db
from datetime import datetime
from db_models.message import Message
from db_models.user import User
from flask_socketio import SocketIO, emit
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "static/profile_pics"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

def allowed_file(filename):
    return "." in filename and \
        filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SECRET_KEY"] = "SECRET_KEY_WEBSOCKET"

db.init_app(app)
socketio = SocketIO(app)

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    
    if username and password:
        user = User.query.filter_by(username=username).first()
        
        if user and bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
            login_user(user)
            return jsonify({"message": "Login successful"})
        
    return jsonify({"error": "Invalid credentials"}), 400

@app.route("/api/user", methods=["POST"])
def create_user():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    
    if password and username:
        hashed_password_bytes = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        
        hashed_password_str = hashed_password_bytes.decode("utf-8")
        
        user = User(username=username, password=hashed_password_str, role="user")
        db.session.add(user)
        db.session.commit()
        return jsonify({ "message": "User created successfully" })
    
    return jsonify({ "error": "Invalid credentials" }), 400

@app.route("/api/upload_photo", methods=["POST"])
@login_required
def upload_photo():
    
        if "foto_perfil" not in request.files:
            return redirect(url_for("index"))
        
        file = request.files["foto_perfil"]
        
        if file.filename == "":
            return redirect(url_for("index"))
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            
            current_user.profile_image = filename
            db.session.commit()
            
            return redirect(url_for("index"))
        
        return redirect(url_for("index"))
        
@app.route("/api/send_message", methods=["POST"])
@login_required
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
@login_required
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