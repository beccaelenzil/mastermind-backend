import requests
import os
from dotenv import load_dotenv
from tabulate import tabulate
import random

load_dotenv()

url = os.environ.get("API_URL")


def get_level_info():
    response = requests.get(url+"levels/")
    level_info = response.json()
    return level_info


def print_level_info():
    level_info = get_level_info()
    print(tabulate([["easy", level_info["easy"]["num"],
                     f'{level_info["easy"]["min"]} - {level_info["easy"]["max"]}'],
                    ["standard", level_info["standard"]["num"],
                     f'{level_info["standard"]["min"]} - {level_info["standard"]["max"]}'],
                    ["hard", level_info["hard"]["num"],
                     f'{level_info["hard"]["min"]} - {level_info["hard"]["max"]}']],
                   headers=["Level", "Number of Digits", "Range of Digits"]))


def generate_code(level):
    level_info = get_level_info()
    code = ""
    for _ in range(level_info[level]["num"]):
        code += str(random.choice(range(level_info[level]
                                        ["min"], level_info[level]["max"]+1)))
    return {"code": code, "max_tries": level_info[level]["max_guesses"]}


def get_level(level):
    if level == "e" or level == "easy":
        return "easy"
    elif level == "h" or level == "hard":
        return "hard"
    else:
        return "standard"


def print_stars():
    print("*********************")
