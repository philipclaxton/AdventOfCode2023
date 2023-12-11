import pathlib

data = pathlib.Path(__file__).parent / "data.txt"

with open(data, "r") as file:
    data = file.readlines()


paths = {}

instructions = data[0].strip()


for line in data[2:]:
    line_parts = line.strip().split(" = ")
    key = line_parts[0]
    line_parts = line_parts[1].replace("(", "").replace(")", "").split(", ")
    left_value = line_parts[0]
    right_value = line_parts[1]

    if key in paths:
        raise Exception("Key already exists")

    paths[key] = {
        "L": left_value,
        "R": right_value,
    }

current_index = 0
current_key = "AAA"
number_of_iterations = 0


while True:
    if current_key == "ZZZ":
        print("Found it")
        break
    number_of_iterations += 1

    current_key = paths[current_key][instructions[current_index]]
    current_index += 1

    # No luck, start the loop again
    if current_index == len(instructions):
        current_index = 0
        print("No luck, start the loop again. Current key:", current_key, "Number of iterations:", number_of_iterations)

print(number_of_iterations)
