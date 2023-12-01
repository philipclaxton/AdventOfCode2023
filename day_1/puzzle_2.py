import re 
import pathlib

data_path = pathlib.Path(__file__).parent / "data.txt"


digits_only = re.compile(r"^(one|two|three|four|five|six|seven|eight|nine|\d)")

with open(data_path, "r") as file:
    data = file.readlines()

numbers = []

sum = 0

digits_map = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}

for line in data:

    print("line: ", line)

    digits = []

    for index in range(len(line)):
        matches = re.match(digits_only, line[index:])
        if matches:
            match = matches.group(1)
            if match in digits_map:
                match = digits_map[match]
            digits.append(match)

    print("digits: ", digits)
    print("digits_only: ", digits)
    print("digits_only[0]: ", digits[0])
    print("digits_only[-1]: ", digits[-1])

    first_digit = digits[0]
    last_digit = digits[-1]

    if first_digit in digits_map:
        first_digit = digits_map[first_digit]
    if last_digit in digits_map:
        last_digit = digits_map[last_digit]

    number = int(first_digit) * 10 + int(last_digit)
    print("number: ", number)

    sum += number



print("sum: ", sum)