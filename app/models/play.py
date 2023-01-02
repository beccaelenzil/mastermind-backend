from app import db

class Play(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def to_json(self):
        return {
            "id": self.id,
            "code": self.code,
            "game_id": self.game_id,
            "user_id": self.user_id,
        }