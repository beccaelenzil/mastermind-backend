from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    username = db.Column(db.String)

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "username": self.username,
        }
