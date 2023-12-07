import pathlib
import math

data = pathlib.Path(__file__).parent / "data.txt"

with open(data, "r") as file:
    data = file.readlines()

race_times = [int(time) for time in data[0].split(":")[1].split()]
record_distances = [int(distance) for distance in data[1].split(":")[1]. split()]

product  = 1

for race_time, record_distance in zip(race_times, record_distances):

    number_of_victories = 0
    d = race_time**2 - 4 * record_distance
    minimum_hold_time = (race_time - math.sqrt(d))/2
    maximum_hold_time = (race_time + math.sqrt(d))/2

    number_of_solutions = math.floor(maximum_hold_time) - math.floor(minimum_hold_time)
    print(number_of_solutions)

    product *= number_of_solutions

print(product)