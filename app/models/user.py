from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.Integer)
    username = db.Column(db.String)
    type = db.Column(db.String)

    def to_json(self):
        return {
            "id": self.id,
            "uid": self.uid,
            "username": self.username,
            "type": self.type,
        }