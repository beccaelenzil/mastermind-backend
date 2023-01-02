from app.models.constants import LEVELS, PARAMS

def validate_code(code, level):
    PARAMS["max"] = LEVELS[level]["max"]

    if len(code) != PARAMS["num"]:
        return False

    for char in code:
        if int(char) < 0 or int(char) > PARAMS["max"]:
            return False

    return True