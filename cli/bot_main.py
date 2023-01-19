from game_functions import *
from bot import *
import requests
import pprint
pp = pprint.PrettyPrinter(indent=4)

url = os.environ.get("API_URL")

print_intro()
[level, MAX_TRIES] = get_and_print_level()
print("Let's play!")
play = "Y"
user_id = None
initial_guesses = initialize_guesses(level)
play_num = 0
number_freq = {}
while play == "Y":
    [turn, code, guess, guesses, game_id, status_code, code_guesses] = initialize()

    while code != guess and turn < MAX_TRIES:
        while status_code != 201:
            if play_num < len(initial_guesses):
                guess = initial_guesses[play_num]
            else:
                guess = generate_code(level, number_freq, code_guesses)
            response = requests.post(f"{url}plays/",
                                     json={"code": guess, "level": level, "game_id": game_id, "user_id": user_id})
            status_code = response.status_code
            if status_code != 201:
                response_body = response.json()
                print(response_body["error"])

        response_body = response.json()
        code_guesses.append(guess)
        guesses.append([guess, response_body["correct_nums"],
                       response_body["correct_pos"]])
        code = response_body["answer"]
        if play_num < len(initial_guesses):
            number_freq = update_number_freq(
                guess, response_body["correct_nums"], number_freq)

        play_num += 1

        # get game info on first play
        if not game_id:
            game_id = response_body["game_id"]

        turn += 1
        if response_body["win"]:
            print_play_info(guesses)
            print("The bot guessed it!")
            print("The code was... ", code)
            initial_guesses = initialize_guesses(level)
            play_num = 0
            [play, game_id] = play_again()
        elif turn == MAX_TRIES:
            print_play_info(guesses)
            print("The bot ran out of guesses.")
            print("The code was... ", code)
            initial_guesses = initialize_guesses(level)
            play_num = 0
            [play, game_id] = play_again()
        else:
            guess = "XXXX"
            status_code = 400

        if user_id and play != "Y":
            response = requests.get(f"{url}users/{user_id}")
            response_body = response.json()

            pp.pprint(response_body["performance summary"])


print("Thanks for playing!")
