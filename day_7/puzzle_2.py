import pathlib

data = pathlib.Path(__file__).parent / "data.txt"

with open(data, "r") as file:
    data = file.readlines()


card_strength_map = {
    "J": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "T": 10,
    "Q": 12,
    "K": 13,
    "A": 14,
}

hand_strength_map = {
    "five_of_a_kind": 7,
    "four_of_a_kind": 6,
    "full_house": 5,
    "three_of_a_kind": 4,
    "two_pair": 3,
    "one_pair": 2,
    "high_card": 1,
}
result_list = []


def get_value_of_hand(cards: dict[str, int]) -> int:
    match len(cards.keys()):
        case 5:
            hand_type = "high_card"
        case 4:
            hand_type = "one_pair"
        case 3:
            if 3 in [value["count"] for value in cards.values()]:
                hand_type = "three_of_a_kind"
            else:
                hand_type = "two_pair"
        case 2:
            if 4 in [value["count"] for value in cards.values()]:
                hand_type = "four_of_a_kind"
            else:
                hand_type = "full_house"
        case 1:
            hand_type = "five_of_a_kind"
        case _:
            raise Exception("Invalid hand")

    return hand_strength_map[hand_type] * 16**5


for line in data:
    hand, bid = line.split()

    cards = {}

    hand_strength = 0

    # Calculate the strength of the cards based on their position in the hand
    for index, card in enumerate(hand):
        if card not in cards:
            cards[card] = {
                "count": 1,
                "strength": card_strength_map[card],
                "index": index,
            }
        else:
            cards[card]["count"] += 1
        hand_strength = hand_strength * 16 + card_strength_map[card]

    # Substitute jacks for the most common card
    if "J" in cards:
        number_of_jacks = cards["J"]["count"]
        if number_of_jacks < 5:
            del cards["J"]
            most_common_card = sorted(cards, key=lambda x: cards[x]["count"])[-1]
            cards[most_common_card]["count"] += number_of_jacks

    # Calculate the strength of the hand type
    hand_strength += get_value_of_hand(cards)
    result_list.append((hand_strength, bid))


sorted_results = sorted(result_list, key=lambda x: x[0])

score = 0

for index, (_, bid) in enumerate(sorted_results):
    score += (index + 1) * int(bid)

print(score)
