import pathlib

data = pathlib.Path(__file__).parent / "data.txt"

with open(data, "r") as file:
    data = file.readlines()

MAX_RED = 12
MAX_GREEN = 13
MAX_BLUE = 14


def too_many(dice_result, max):
    return int(dice_result.split()[0]) > max


possible_games = set()

for line in data:
    game_info, results = line.split(":")

    game_number = int(game_info.split()[-1])

    results = results.split(";")

    possible = True

    for result in results:
        dice_results = result.split(",")

        for dice_result in dice_results:
            if "red" in dice_result and too_many(dice_result, MAX_RED):
                possible = False
                break
            if "green" in dice_result and too_many(dice_result, MAX_GREEN):
                possible = False
                break
            if "blue" in dice_result and too_many(dice_result, MAX_BLUE):
                possible = False
                break
        if not possible:
            break
    if possible:
        possible_games.add(game_number)


print(possible_games)
print(sum(possible_games))
