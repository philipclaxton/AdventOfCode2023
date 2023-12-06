import pathlib

data = pathlib.Path(__file__).parent / "data.txt"

with open(data, "r") as file:
    data = file.readlines()


powers = []

for line in data:
    game_info, results = line.split(":")

    game_number = int(game_info.split()[-1])

    results = results.split(";")

    max_red = 0
    max_green = 0
    max_blue = 0

    for result in results:
        dice_results = result.split(",")

        for dice_result in dice_results:
            if "red" in dice_result:
                max_red = max(max_red, int(dice_result.split()[0]))
            if "green" in dice_result:
                max_green = max(max_green, int(dice_result.split()[0]))
            if "blue" in dice_result:
                max_blue = max(max_blue, int(dice_result.split()[0]))

    powers.append(max_red * max_green * max_blue)

print(powers)
print(sum(powers))
