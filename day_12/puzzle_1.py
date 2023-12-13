import pathlib

data = pathlib.Path(__file__).parent / "data_sample.txt"

with open(data, "r") as file:
    data = file.readlines()

processed_data = []

for line in data:
    # First thing we want to do is trim off the operational gears at the beginning and end

    parts = line.split()
    pattern = parts[0]
    numbers = parts[1].split(",")

    pattern = pattern.strip(".")

    processed_data.append({"pattern": pattern, "numbers": numbers})


with open("processed_data.txt", "w") as file:
    for entry in processed_data:
        line = f"{entry['pattern']} "
        line += ",".join(entry["numbers"])
        file.write(line + "\n")
