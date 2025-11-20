from flask import Flask, jsonify, request, render_template
from repository.database import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SECRET_KEY"] = "SECRET_KEY_WEBSOCKET"

db.init_app(app)

if __name__ == "__main__":
    app.run(debug=True)