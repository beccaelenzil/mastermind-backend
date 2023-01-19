from game_functions import *
from collections import Counter
import copy
level = "easy"


def initialize_guesses(level):
    level_info = get_level_info()
    initial_guesses = []
    for number in range(level_info[level]
                        ["min"], level_info[level]["max"]+1):
        initial_guesses.append(str(number)*level_info[level]["num"])

    return initial_guesses


def initialize_number_freq(level):
    level_info = get_level_info()
    number_freq = {}
    for number in range(level_info[level]
                        ["min"], level_info[level]["max"]+1):
        number_freq[number] = level_info[level]["num"]
    return number_freq


def update_number_freq(guess, cor_nums, number_freq):
    number_freq[guess[0]] = cor_nums
    return number_freq


def generate_code(level, number_freq, guesses):
    level_info = get_level_info()
    code = guesses[0]
    while code in guesses:
        code = ""
        count = 0
        number_freq_copy = copy.copy(number_freq)
        while count < level_info[level]["num"]:
            number = str(random.choice(list(number_freq_copy.keys())))
            if number_freq_copy[number] > 0:
                code += number
                number_freq_copy[number] -= 1
                count += 1

    return code
