import pathlib
import numpy as np

data = pathlib.Path(__file__).parent / "data.txt"

with open(data, "r") as file:
    lines = file.readlines()

data = [] 
for index, line in enumerate(lines):
    data.append(list(line.strip()))

def get_rows_without_galaxy(data):
    rows = []
    for index, row in enumerate(data):
        if "#" not in row:
            rows.append(index)
    return rows

data = np.array(data)
galaxy_coordinates = []

for row_index in range(len(data)):
    for col_index in range(len(data[0])):
        if data[row_index][col_index] == "#":
            galaxy_coordinates.append([row_index, col_index])


for galaxy_index, galaxy_coordinate in enumerate(galaxy_coordinates):
    v_expansion = 0
    h_expansion = 0

    for value in get_rows_without_galaxy(data):
        if galaxy_coordinate[0] > value:
            v_expansion += 1
        else:
            break
    for value in get_rows_without_galaxy(np.transpose(data)):
        if galaxy_coordinate[1] > value:
            h_expansion += 1
        else:
            break
    if v_expansion > 0:
        galaxy_coordinates[galaxy_index][0] += (v_expansion * (1000000 - 1))
    if h_expansion > 0:
        galaxy_coordinates[galaxy_index][1] += (h_expansion * (1000000 - 1))

min_distances = []

while len(galaxy_coordinates) > 0:
    galaxy_coordinate = galaxy_coordinates.pop(0)
    
    for galaxy_coordinate_2 in galaxy_coordinates:
        min_distances.append(abs(galaxy_coordinate[0] - galaxy_coordinate_2[0]) + abs(galaxy_coordinate[1] - galaxy_coordinate_2[1]))

print(sum(min_distances))
    