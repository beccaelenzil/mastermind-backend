from game_functions import *
import requests

MAX_TRIES = 10

print("Welcome to MASTERMIND")
print("Your job is to guess the sequence of four digits")
print("*********************")
print("There are 4 distinct digits in easy mode, 8 digits in standard mode, and 10 digits in hard mode.")
level = input("Would you like to play easy(e), standard(s), or in hard(h) mode? ")
[level, example] = get_level(level)
print(level.upper(), "mode it is!")
print("*********************")
print("An example string is: ", example)
print("Let's play!")
play = "Y"

while play == "Y":
    turn = 0
    code = "YYYY"
    guess = "XXXX"
    guesses = []
    game_id = None
    
    while code != guess and turn < MAX_TRIES:
        response = requests.post(f"http://127.0.0.1:5000/plays/", json={"code": guess, "level": level, "game_id": game_id})
        while response.status_code != 201:
            guess = input("Guess the sequence: ")
            response = requests.post(f"http://127.0.0.1:5000/plays/", json={"code": guess, "level": level, "game_id": game_id})
            if response.status_code != 201:
                print(response)
                print("Thank was not a valid guess")
        
        response_body = response.json()
        guesses.append([guess, response_body["correct_nums"], response_body["correct_pos"]])
        if not game_id:
            game_id = response_body["game_id"]
            game_response = requests.get(f'http://127.0.0.1:5000/games/{game_id}')
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
