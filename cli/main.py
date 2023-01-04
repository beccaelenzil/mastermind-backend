from game_functions import *
import requests


print("Welcome to MASTERMIND")
print("Your job is to guess the sequence of a series of digits")
print_stars()
print("You can play in easy, standard, or hard mode.")
print_stars()
level_info = print_level_info()
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
print("Let's play!")
play = "Y"
while play == "Y":
    turn = 0
    code = "YYYY"
    guess = "XXXX"
    guesses = []
    game_id = None

    while code != guess and turn < MAX_TRIES:
        response = requests.post(f"http://127.0.0.1:5000/plays/",
                                 json={"code": guess, "level": level, "game_id": game_id})
        while response.status_code != 201:
            guess = input("Guess the sequence: ")
            response = requests.post(f"http://127.0.0.1:5000/plays/",
                                     json={"code": guess, "level": level, "game_id": game_id})
            if response.status_code != 201:
                print(response)
                print("Thank was not a valid guess")

        response_body = response.json()
        guesses.append([guess, response_body["correct_nums"],
                       response_body["correct_pos"]])
        if not game_id:
            game_id = response_body["game_id"]
            game_response = requests.get(
                f'http://127.0.0.1:5000/games/{game_id}')
            game_response_body = game_response.json()
            code = game_response_body["code"]

        print("|# | CODE | N | N&P |")
        print("|--|------|---|-----|")
        for i in range(len(guesses)):
            g = guesses[i]
            print(i+1, ")", g[0], " ", g[1], " ", g[2])

        turn += 1
        if response_body["win"]:
            print("You guessed it!")
            print("The code was...")
            print(guess)
            play = input("Play again? Y or N: ")
            play = play.upper()
            game_id = None
        elif turn == MAX_TRIES:
            print("You ran out of guesses. The code was...")
            print(code)
            play = input("Play again? Y or N: ")
            play = play.upper()
            game_id = None
        else:
            guess = "XXXX"


print("Thanks for playing!")
