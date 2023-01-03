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
    response = requests.post("http://127.0.0.1:5000/games/",json={"level": level})
    if response.status_code == 201:
        response_body = response.json()
        code = response_body["code"]
        game_id = response_body["id"]
        print("The code is ", response_body["code"])
    else:
        print("There was a problem generating a code", response)

    turn = 0
    guess = "XXXX"
    guesses = []
    
    while code != guess and turn < MAX_TRIES:
        response = requests.post(f"http://127.0.0.1:5000/games/{game_id}/plays", json={"code": guess})
        while response.status_code != 201:
            guess = input("Guess the sequence: ")
            response = requests.post(f"http://127.0.0.1:5000/games/{game_id}/plays", json={"code": guess})
            if response.status_code != 201:
                print("Thank was not a valid guess")
        
        response_body = response.json()
        guesses.append([guess, response_body["correct_nums"], response_body["correct_pos"]])

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
        elif turn == MAX_TRIES:
            print("You ran out of guesses. The code was...")
            print(code)
            play = input("Play again? Y or N: ")
            play = play.upper()
        else:
            guess = "XXXX"

print("Thanks for playing!")
