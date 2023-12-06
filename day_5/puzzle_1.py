import pathlib

data = pathlib.Path(__file__).parent / "data_sample.txt"

with open(data, "r") as file:
    data = file.readlines()

seeds = [int(number) for number in data[0].split(":")[1].split()]


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

for seed in seeds:
    soil = find_in_map(seed, maps["seed"]["soil"])
    fertilzer = find_in_map(soil, maps["soil"]["fertilizer"])
    water = find_in_map(fertilzer, maps["fertilizer"]["water"])
    light = find_in_map(water, maps["water"]["light"])
    temperature = find_in_map(light, maps["light"]["temperature"])
    humidity = find_in_map(temperature, maps["temperature"]["humidity"])
    location = find_in_map(humidity, maps["humidity"]["location"])

    if lowest_location is None or location < lowest_location:
        lowest_location = location

    # print(min(soil, fertilzer, water, light, temperature, humidity, location))

print(lowest_location)

# exit(0)


# for input in maps:
#     for output in maps[input]:
#         print(input, output)
#         print(maps[input][output])
