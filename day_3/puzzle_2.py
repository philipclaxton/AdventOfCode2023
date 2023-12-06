import pathlib
import re

from itertools import chain

DIGITS = re.compile(r"\d+")

data = pathlib.Path(__file__).parent / "data.txt"

with open(data, "r") as file:
    data = file.readlines()

MIN_ROWS = 0
MAX_ROWS = len(data) - 1

part_numbers = []


def search_line_for_number(line: str, index: int):
    if line[index].isdigit():
        start_index = index
        end_index = index

        while True and start_index > 0:
            if line[start_index - 1].isdigit():
                start_index -= 1
            else:
                break

        while True and end_index < len(line) - 1:
            if line[end_index + 1].isdigit():
                end_index += 1
            else:
                break

        return int(line[start_index : end_index + 1])
    return None


def get_numbers_from_line(line: str, first_index: int):
    first_number = search_line_for_number(line, first_index)
    second_number = None

    if first_number is None:
        first_number = search_line_for_number(line, first_index + 1)
        if first_number is None:
            first_number = search_line_for_number(line, first_index + 2)
    elif not line[first_index + 1].isdigit():
        second_number = search_line_for_number(line, first_index + 2)

    return first_number, second_number


product_sum = 0

for line_index, line in enumerate(data):
    starting_index = None
    current_index = None

    in_number = False

    line_part_numbers = []

    for index, char in enumerate(data[line_index]):
        if char == "*":
            adjacent_numbers = []

            if line_index > 0:
                adjacent_numbers += get_numbers_from_line(
                    data[line_index - 1], index - 1
                )
            adjacent_numbers += get_numbers_from_line(data[line_index], index - 1)
            if line_index < len(data) - 1:
                adjacent_numbers += get_numbers_from_line(
                    data[line_index + 1], index - 1
                )

            adjacent_numbers = list(filter(lambda x: x is not None, adjacent_numbers))

            if len(adjacent_numbers) == 2:
                gear_ratio = adjacent_numbers[0] * adjacent_numbers[1]
                print(f"Gear ratio: {gear_ratio}")
                product_sum += gear_ratio


print(product_sum)
