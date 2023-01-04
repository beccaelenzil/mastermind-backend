from app import db


class User(db.Model):
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    username = db.Column(db.String)

    def to_json(self):
        return {
            "uid": self.uid,
            "name": self.name,
            "username": self.username,
        }
