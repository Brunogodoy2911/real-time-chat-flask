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
from flask_cors import CORS

UPLOAD_FOLDER = "static/profile_pics"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

def allowed_file(filename):
    return "." in filename and \
        filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SECRET_KEY"] = "SECRET_KEY_WEBSOCKET"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

CORS(app)

db.init_app(app)
socketio = SocketIO(app, cors_allowed_origins="*")

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

@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/api/user", methods=["POST"])
def create_user():
    username = request.form.get("username")
    password = request.form.get("password")
    file = request.files.get("avatar")
    
    if password and username:
        hashed_password_bytes = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        
        hashed_password_str = hashed_password_bytes.decode("utf-8")
        
        filename = None
        if file:
            filename = secure_filename(file.filename)
            save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(save_path)
            
        user = User(username=username, password=hashed_password_str, profile_image=filename)
        db.session.add(user)
        db.session.commit()
        return jsonify({ "message": "User created successfully" })
    
    return jsonify({ "error": "Invalid credentials" }), 400

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("login_page"))

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

    new_message = Message(content=data["content"], timestamp=timestamp, username=current_user.username)

    db.session.add(new_message)
    db.session.commit()
    
    message_data = {
        "username": current_user.username,
        "content": data["content"],
        "timestamp": timestamp.strftime("%H:%M")
    }
    
    socketio.emit("message", message_data)

    return jsonify({"message": "The message was sent successfully", "data": new_message.to_dict()}), 201

@app.route("/api/messages", methods=["GET"])
@login_required
def get_messages():
    messages = Message.query.order_by(Message.timestamp.desc()).all()
    messages_list = [message.to_dict() for message in messages]
    
    for msg in messages:
        user = User.query.filter_by(username=msg.username).first()
        
        if user and user.profile_image:
            avatar = f"/static/profile_pics/{user.profile_image}"
        else:
            avatar = "https://ik.imagekit.io/brunogodoy/default"
        
        msg_dict = msg.to_dict()
        msg_dict["avatar"] = avatar
        messages_list.append(msg_dict)
    
    return jsonify(messages_list), 200

@app.route("/", methods=["GET"])
def index():
    
    if current_user.is_authenticated:
        username = current_user.username
    else:
        username = "Visitante"
   
    return render_template("index.html", username=username)

@socketio.on("message")
def handle_message(data):

    if "content" not in data:
        emit("error", {"message": "Content is required"}, room=request.sid)
        return False
    
    username = data.get("username", "Anônimo")
    content = data["content"]
    timestamp = datetime.now()

    with current_app.app_context():
        new_message = Message(content=content, timestamp=timestamp, username=username)
        db.session.add(new_message)
        db.session.commit()
        
        if current_user.is_authenticated and current_user.profile_image:
            avatar = f"/static/profile_pics/{current_user.profile_image}"
        else:
            avatar = "https://ik.imagekit.io/brunogodoy/default"
        
        message_data = {
                "username": username,
                "content": content,
                "timestamp": timestamp.strftime("%H:%M"),
                "avatar": avatar
            }
        emit("message", message_data, broadcast=True)
    
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    socketio.run(app, debug=True)