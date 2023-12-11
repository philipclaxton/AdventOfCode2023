import pathlib

data = pathlib.Path(__file__).parent / "data.txt"

with open(data, "r") as file:
    data = file.readlines()


def find_next_number(numbers: list[int]) -> int:
    new_row = []
    all_zeros = True

    for i in range(1, len(numbers)):
        diff = numbers[i] - numbers[i - 1]
        all_zeros &= diff == 0
        new_row.append(diff)
    if all_zeros:
        return numbers[-1]
    return numbers[-1] + find_next_number(new_row)


sum_of_next_numbers = 0

for line in data:
    numbers = [int(x) for x in line.split()]

    next_number = find_next_number(numbers)
    sum_of_next_numbers += next_number
    print(next_number)

print("Sum of the next numbers: ", sum_of_next_numbers)
