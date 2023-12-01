import re 
import pathlib

data_path = pathlib.Path(__file__).parent / "data.txt"

not_digits = re.compile(r"[^\d]")

with open(data_path, "r") as file:
    data = file.readlines()

numbers = []

sum = 0

for line in data:

    digits_only = re.sub(not_digits, "", line)

    print("digits_only: ", digits_only)
    print("digits_only[0]: ", digits_only[0])
    print("digits_only[-1]: ", digits_only[-1])

    number = int(digits_only[0]) * 10 + int(digits_only[-1])
    print("number: ", number)

    sum += number



print("sum: ", sum)