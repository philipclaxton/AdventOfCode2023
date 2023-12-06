import functools
import pathlib


data = pathlib.Path(__file__).parent / "data.txt"

with open(data, "r") as file:
    data = file.readlines()


total_cards = 0


@functools.lru_cache(maxsize=1000)
def process_card(card_index: int):
    print("processing Card", card_index + 1)

    number_of_cards = 1

    card = data[card_index]

    elf_numbers, winning_numbers = card.split(":")[1].split("|")

    elf_numbers = elf_numbers.split()
    winning_numbers = winning_numbers.split()

    new_cards = 0

    for elf_number in elf_numbers:
        if elf_number in winning_numbers:
            new_cards += 1

    if new_cards > 0:
        print(f"Win {new_cards} cards")
        for new_index in range(card_index + 1, card_index + new_cards + 1):
            number_of_cards += process_card(new_index)

    return number_of_cards


for line_index, _ in enumerate(data):
    cards_in_line = process_card(line_index)
    total_cards += cards_in_line

    print(f'Done with {data[line_index].split(":")[0]}. {cards_in_line} cards in line.')

print(total_cards)
