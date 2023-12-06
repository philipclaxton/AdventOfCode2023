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

for line_index, line in enumerate(data):
    starting_index = None
    current_index = None

    in_number = False

    line_part_numbers = []

    for index, char in enumerate(data[line_index]):
        if char.isdigit():
            if starting_index is None:
                starting_index = index
            current_index = index
            in_number = True
        elif in_number:
            possible_part_number = int(line[starting_index : current_index + 1])

            characters_to_search = ""

            first_search_index = (
                starting_index - 1 if starting_index > 0 else starting_index
            )
            last_search_index = (
                current_index + 1 if current_index < len(line) else current_index
            )

            characters_to_search += line[first_search_index]
            characters_to_search += line[last_search_index]

            if line_index > 0:
                characters_to_search += data[line_index - 1][
                    first_search_index : last_search_index + 1
                ]
                print(data[line_index - 1][first_search_index : last_search_index + 1])
            print(data[line_index][first_search_index : last_search_index + 1])
            if line_index < len(data) - 1:
                characters_to_search += data[line_index + 1][
                    first_search_index : last_search_index + 1
                ]
                print(data[line_index + 1][first_search_index : last_search_index + 1])

            characters_to_search = characters_to_search.replace("\n", "")
            characters_to_search = characters_to_search.replace(".", "")
            characters_to_search = re.sub(DIGITS, "", characters_to_search)

            if len(characters_to_search) > 0:
                print(f"{possible_part_number} is a part number")
                line_part_numbers.append(possible_part_number)
            else:
                print(f"{possible_part_number} is NOT a part number")
            starting_index = None
            current_index = None
            in_number = False

    part_numbers.append(line_part_numbers)
    print(f"line number: {line_index}, part numbers: {line_part_numbers}\n\n")

    # exit(0)

    # print(part_numbers)

all_part_numbers = list(chain.from_iterable(part_numbers))

print(sum(all_part_numbers))


# print(sum(part_numbers))
