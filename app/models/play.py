from app import db
from collections import Counter
from app.models.level import Level


class Play(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))

    def to_json(self):
        return {
            "id": self.id,
            "code": self.code,
            "game_id": self.game_id,
            "correct_nums": self.correct_nums(),
            "correct_pos": self.correct_pos(),
            "win": self.win(),
            "answer": self.display_answer_code()
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
        return self.code == self.game.code

    def display_answer_code(self):
        level = Level.query.get(self.game.level_id)
        if not level:
            return None
        params = level.params()
        max_guesses = params["max_guesses"]
        if self.win() or len(self.game.plays) == max_guesses:
            return self.game.code
        else:
            return "hidden"
