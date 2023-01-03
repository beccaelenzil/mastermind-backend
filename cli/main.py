from game_functions import *
import requests

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
        print("The code is ", response_body["code"])
    else:
        print("There was a problem generating a code", response)
    
    play = input("Would you like to play again? Yes(Y) or No(N): ")
    play = play.upper()

print("Thanks for playing!")
