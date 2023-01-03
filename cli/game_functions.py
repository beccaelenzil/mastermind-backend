
#TODO: update sample codes with constants from PARAMS
def get_level(level):
    if level == "e" or level == "easy":
        return ["easy", "1102"]
    elif level == "h" or level == "hard":
        return ["hard", "9800"]
    else:
        return ["standard", "6752"]


