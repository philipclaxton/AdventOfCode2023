import pathlib

data = pathlib.Path(__file__).parent / "data.txt"

with open(data, "r") as file:
    data = file.readlines()

seed_values = [int(number) for number in data[0].split(":")[1].split()]

seeds = [(start, range) for start, range in zip(*[iter(seed_values)] * 2)]


def find_in_map(input, map):
    for entry in map:
        destination, source, length = entry
        if input >= source and input < source + length:
            return destination + input - source
    return input


maps = {}

input = None
output = None
value_lines = []

for index, line in enumerate(data):
    current_map = {}

    if len(line) == 1 or index == len(data) - 1:
        if input is not None and output is not None:
            value_lines = sorted(value_lines, key=lambda x: x[0])
            if input not in maps:
                maps[input] = {}
            maps[input][output] = value_lines
        input = None
        output = None
        value_lines = []
        continue

    if "map" in line:
        parts = line.split()[0].split("-to-")
        input = parts[0]
        output = parts[1]
        continue

    if input is not None and output is not None:
        value_lines.append([int(number) for number in line.split()])

lowest_location = None

# This search algorithm is straight up terrible. It literally takes hours to run.
# If this was a real world problem, I'd be looking for a better algorithm.

# Binary search would be a good start, but I could also process the data to create a
# single map that would allow me to find the location in a single step.

for initial_seed, number_of_seeds in seeds:
    seed = initial_seed

    print(f"Starting with seed {seed}...")
    while seed < initial_seed + number_of_seeds:
        soil = find_in_map(seed, maps["seed"]["soil"])
        fertilzer = find_in_map(soil, maps["soil"]["fertilizer"])
        water = find_in_map(fertilzer, maps["fertilizer"]["water"])
        light = find_in_map(water, maps["water"]["light"])
        temperature = find_in_map(light, maps["light"]["temperature"])
        humidity = find_in_map(temperature, maps["temperature"]["humidity"])
        location = find_in_map(humidity, maps["humidity"]["location"])

        if lowest_location is None or location < lowest_location:
            lowest_location = location

        seed += 1
    print(f"done")

print(lowest_location)
