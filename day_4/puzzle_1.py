import pathlib

data = pathlib.Path(__file__).parent / "data.txt"

with open(data, "r") as file:
    data = file.readlines()


total_score = 0

for line in data:
    elf_numbers, winning_numbers = line.split(":")[1].split("|")

    elf_numbers = elf_numbers.split()
    winning_numbers = winning_numbers.split()

    round_score = 0

    for elf_number in elf_numbers:
        if elf_number in winning_numbers:
            if round_score == 0:
                round_score = 1
            else:
                round_score = round_score * 2

    total_score += round_score

print(total_score)
