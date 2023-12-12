import pathlib
import numpy as np

data = pathlib.Path(__file__).parent / "data.txt"

with open(data, "r") as file:
    lines = file.readlines()

data = [] 
for index, line in enumerate(lines):
    data.append(list(line.strip()))


def expand_rows(data):
    data_copy = []
    for row in data:
        data_copy.append(row)
        if "#" not in row:
            data_copy.append(row)
    return data_copy

data = np.array(data)
data = expand_rows(data)
data = np.transpose(data)
data = expand_rows(data)
data = np.transpose(data)

galaxy_coordinates = []

for row_index in range(len(data)):
    for col_index in range(len(data[0])):
        if data[row_index][col_index] == "#":
            galaxy_coordinates.append([row_index, col_index])

min_distances = []

while len(galaxy_coordinates) > 0:
    galaxy_coordinate = galaxy_coordinates.pop(0)
    
    for galaxy_coordinate_2 in galaxy_coordinates:
        min_distances.append(abs(galaxy_coordinate[0] - galaxy_coordinate_2[0]) + abs(galaxy_coordinate[1] - galaxy_coordinate_2[1]))

print(sum(min_distances))
    