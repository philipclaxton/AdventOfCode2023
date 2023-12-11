from __future__ import annotations

import pathlib

from dataclasses import dataclass


data = pathlib.Path(__file__).parent / "data.txt"

with open(data, "r") as file:
    data = file.readlines()


@dataclass
class Coordinate:
    x: int
    y: int

    def __add__(self, other: Coordinate) -> Coordinate:
        return Coordinate(self.x + other.x, self.y + other.y)

    def __eq__(self, other: Coordinate) -> bool:
        return self.x == other.x and self.y == other.y


NORTH = Coordinate(0, -1)
SOUTH = Coordinate(0, 1)
WEST = Coordinate(-1, 0)
EAST = Coordinate(1, 0)
NONE = Coordinate(0, 0)


def lookup_pipe(location: Coordinate) -> str:
    try:
        return data[location.y][location.x]
    except IndexError:
        raise ValueError(f"Invalid location: {location}")


def get_next_move_from_pipe(pipe: str) -> Coordinate:
    match pipe:
        case "|":
            return SOUTH
        case "-":
            return EAST
        case "L":
            return NORTH + EAST
        case "J":
            return NORTH + WEST
        case "7":
            return SOUTH + WEST
        case "F":
            return SOUTH + EAST
        case "S":
            print("Return to start")
            return NONE  # We've reached the end of the pipe
        case _:
            return NONE
            raise ValueError(f"Invalid pipe: {pipe}")


def get_new_direction(
    pipe_direction: Coordinate, entry_direction: Coordinate
) -> Coordinate:
    # Straight Pipes
    if pipe_direction.x == 0 or pipe_direction.y == 0:
        return entry_direction

    # Corner Pipes
    if entry_direction.x == 0:
        return Coordinate(pipe_direction.x, 0)
    if entry_direction.y == 0:
        return Coordinate(0, pipe_direction.y)

    raise ValueError(
        "Unable to determine new direction", pipe_direction, entry_direction
    )


def is_move_possible(move_direction: Coordinate, new_square: Coordinate) -> bool:
    if move_direction.x == 0:
        # We only need to look for Y moves
        if new_square.y == 0:
            return False  # This is a horizontal pipe, and we can't move vertically
        if new_square.x == 0:
            return True  # This is a vertical pipe, and we can always move vertically
        return (
            move_direction.y == -1 * new_square.y
        )  # If the direction is the same as the new square, we can move there
    elif move_direction.y == 0:
        # We only need to look for Y moves
        if new_square.x == 0:
            return False  # This is a horizontal pipe, and we can't move vertically
        if new_square.y == 0:
            return True  # This is a vertical pipe, and we can always move vertically
        return (
            move_direction.x == -1 * new_square.x
        )  # If the direction is the same as the new square, we can move there
    else:
        raise ValueError("Moves must be in a cardinal direction")


def proceed_through_pipe(
    start_position: Coordinate, entry_direction: Coordinate
) -> tuple[Coordinate, Coordinate]:
    next_position = start_position + entry_direction
    next_pipe_move = get_next_move_from_pipe(lookup_pipe(next_position))
    if entry_direction == NONE or next_pipe_move == NONE:
        print("Exit 1")
        print("Start pipe: ", lookup_pipe(start_position))
        print("Start position: ", start_position)
        print("Entry direction: ", entry_direction)
        print("Next pipe: ", lookup_pipe(next_position))
        print("Next position: ", next_position)
        print("Next pipe move: ", next_pipe_move)
        return None, None

    if is_move_possible(entry_direction, next_pipe_move):
        next_direction = get_new_direction(next_pipe_move, entry_direction)
        return next_position, next_direction
    else:
        print("Exit 2")
        print("Start pipe: ", lookup_pipe(start_position))
        print("Start position: ", start_position)
        print("Entry direction: ", entry_direction)
        print("Next pipe: ", lookup_pipe(next_position))
        print("Next position: ", next_position)
        print("Next pipe move: ", next_pipe_move)
        return None, None


for index, line in enumerate(data):
    if "S" in line:
        start = Coordinate(line.index("S"), index)
        break

number_of_steps_list = []

for next_move in [NORTH, SOUTH, WEST, EAST]:
    number_of_steps = 0
    next_square = start + next_move

    next_pipe = lookup_pipe(next_square)
    next_pipe_direction = get_next_move_from_pipe(next_pipe)

    if is_move_possible(next_move, next_pipe_direction):
        number_of_steps += 1

        next_direction = get_new_direction(next_pipe_direction, next_move)

        while next_square is not None:
            number_of_steps += 1
            next_square, next_direction = proceed_through_pipe(
                next_square, next_direction
            )
    if number_of_steps > 0:
        number_of_steps_list.append(number_of_steps)

if len(number_of_steps_list) == 2:
    # Good loop

    print(number_of_steps_list[0] / 2)

print(start)
