from repository.database import db

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

def tp_dict(self):
    return {
        "id": self.id,
        "content": self.content,
        "timestamp": self.timestamp.isoformat(),
    }