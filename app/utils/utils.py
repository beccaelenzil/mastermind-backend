from app.models.constants import LEVELS, PARAMS, RANDOM_URL
from collections import Counter
import requests

def return_params(level):
    PARAMS["max"] = LEVELS[level]["max"]
    return PARAMS

def validate_code(code, level):
    PARAMS = return_params(level)

    if len(code) != PARAMS["num"]:
        return False

    for char in code:
        try:
            i = int(char)
        except:
            return False

        if i < 0 or int(char) > PARAMS["max"]:
            return False
            

    return True







