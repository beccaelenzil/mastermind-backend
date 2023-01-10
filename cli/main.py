from game_functions import *
import requests
import pprint
pp = pprint.PrettyPrinter(indent=4)

url = os.environ.get("API_URL")

print_intro()
[level, MAX_TRIES] = get_and_print_level()
user_id = login()
print("Let's play!")
play = "Y"
while play == "Y":
    [turn, code, guess, guesses, game_id, status_code] = initialize()

    while code != guess and turn < MAX_TRIES:
        while status_code != 201:
            guess = input("Guess the sequence: ")
            response = requests.post(f"{url}plays/",
                                     json={"code": guess, "level": level, "game_id": game_id, "user_id": user_id})
            status_code = response.status_code
            if status_code != 201:
                response_body = response.json()
                print(response_body["error"])
        response_body = response.json()
        guesses.append([guess, response_body["correct_nums"],
                       response_body["correct_pos"]])

        # get game info on first play
        if not game_id:
            game_id = response_body["game_id"]
            game_response = requests.get(
                f'{url}games/{game_id}')
            game_response_body = game_response.json()
            code = game_response_body["code"]

        # print play info
        print_play_info(guesses)

        turn += 1
        if response_body["win"]:
            print("You guessed it!")
            print("The code was... ", code)
            [play, game_id] = play_again()
        elif turn == MAX_TRIES:
            print("You ran out of guesses.")
            print("The code was... ", code)
            [play, game_id] = play_again()
        else:
            guess = "XXXX"
            status_code = 400

        if user_id and play != "Y":
            response = requests.get(f"{url}users/{user_id}")
            response_body = response.json()

            pp.pprint(response_body["performance summary"])


print("Thanks for playing!")
