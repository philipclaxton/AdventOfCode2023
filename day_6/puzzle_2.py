import pathlib
import math

data = pathlib.Path(__file__).parent / "data.txt"

with open(data, "r") as file:
    data = file.readlines()


race_time = int("".join(data[0].split(":")[1].split()))
record_distance = int("".join(data[1].split(":")[1].split()))
print(race_time, record_distance)


d = race_time**2 - 4 * record_distance

minimum_hold_time = (race_time - math.sqrt(d))/2
maximum_hold_time = (race_time + math.sqrt(d))/2

number_of_solutions = math.floor(maximum_hold_time) - math.floor(minimum_hold_time)

print(number_of_solutions)