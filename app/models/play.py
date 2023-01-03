from app import db
from collections import Counter

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

    def correct_nums(self):
        code_count = Counter(self.code)
        answer_count = Counter(self.game.code)
        count = 0
        for char in answer_count:
            if char in code_count:
                count += min(answer_count[char], code_count[char])
        return count

    def correct_pos(self):
        count = 0
        for i in range(len(self.code)):
            if self.code[i] == self.game.code[i]:
                count += 1
        return count

    def win(self):
        return self.correct_pos() == len(self.code)