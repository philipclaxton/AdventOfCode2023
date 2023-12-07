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
    for time_held in range(0, race_time):
        distance_travelled = time_held * (race_time - time_held)
        if distance_travelled > record_distance:
            number_of_victories += 1
    print(number_of_victories)

    product *= number_of_victories

print(product)