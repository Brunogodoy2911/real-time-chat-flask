from repository.database import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    profile_image = db.Column(db.String(255), nullable=True, default="")
    role=db.Column(db.String(80), nullable=False, default="https://ik.imagekit.io/brunogodoy/default")
    