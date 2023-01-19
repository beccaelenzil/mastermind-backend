import requests
import os
from dotenv import load_dotenv
from tabulate import tabulate
import random

load_dotenv()

url = os.environ.get("API_URL")


def get_level_info():
    response = requests.get(url+"levels/")
    # if levels response is empty
    if not response.json():
        # seed database with levels
        post_response = requests.post(url+"levels/")
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


def print_intro():
    print("Welcome to MASTERMIND")
    print("Your job is to guess the sequence of a series of digits")
    print_stars()
    print("You can play in easy, standard, or hard mode.")
    print_stars()


def get_and_print_level():
    print_level_info()
    level = input(
        "Would you like to play easy(e), standard(s), or in hard(h) mode? ")
    level = get_level(level)
    print(level.upper(), "mode it is!")
    print_stars()
    print("Here are a few example sequences")
    for _ in range(5):
        print(generate_code(level)["code"])
    print_stars()
    MAX_TRIES = generate_code(level)['max_tries']
    print(f"You have {MAX_TRIES} to guess the sequence!")
    print_stars()
    print("After you enter a guess sequence, the computer will show you two numbers.")
    print("The first number is the amount of correct numbers.")
    print("The second number is the amount of correct numbers in the correct position.")
    print_stars()
    return [level, MAX_TRIES]


def login():
    r = input("Would you like to login to track your progress? Y or N ")
    if r.upper() == "Y":
        email = input("Input a username: ")
        response = requests.post(
            f"{url}users/login", json={"email": email})
        response_body = response.json()
        if response.status_code == 200:
            print(f"Welcome back {email}!")
        elif response.status_code == 201:
            print(f"We created a new user, {email}")

        return response_body["uid"]


def initialize():
    turn = 0
    code = "YYYY"
    guess = "XXXX"
    guesses = []
    code_guesses = []
    game_id = None
    status_code = 400
    return [turn, code, guess, guesses, game_id, status_code, code_guesses]


def print_play_info(guesses):
    # print play info
    print("|# | CODE | N | N&P |")
    print("|--|------|---|-----|")
    for i in range(len(guesses)):
        g = guesses[i]
        print(i+1, ")", g[0], " ", g[1], " ", g[2])


def play_again():
    play = input("Play again? Y or N: ")
    return [play.upper(), None]
