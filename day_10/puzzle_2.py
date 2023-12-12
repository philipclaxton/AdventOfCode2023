from __future__ import annotations

import pathlib


from dataclasses import dataclass
from queue import Queue, Empty

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
        case _:
            return NONE


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
        return None, None
    if is_move_possible(entry_direction, next_pipe_move):
        next_direction = get_new_direction(next_pipe_move, entry_direction)
        return next_position, next_direction
    else:
        return None, None


def get_adjacent_ground_sqaures(square: Coordinate) -> list[Coordinate]:
    squares = []

    for x in range(-1, 2):
        for y in range(-1, 2):
            if x == 0 and y == 0:
                continue
            try:
                if map[square.y + y][square.x + x] == ".":
                    squares.append(Coordinate(square.x + x, square.y + y))
            except IndexError:
                continue
    return squares


data = [list(line.strip()) for line in data]

# Get the starting position
for index, line in enumerate(data):
    if "S" in line:
        start = Coordinate(line.index("S"), index)
        break

# Since we need to track not only where the pipes are but also
# the path, lets double the width and height of the map so we
# can record the additional information
map = [["."] * len(data[0]) * 2 for _ in range(len(data) * 2)]

# Mark the starting location on the map
map[start.y * 2][start.x * 2] = "S"

for next_move in [NORTH, SOUTH, WEST, EAST]:
    next_square = start + next_move
    next_pipe = lookup_pipe(next_square)
    next_pipe_direction = get_next_move_from_pipe(next_pipe)

    if is_move_possible(next_move, next_pipe_direction):
        # Okay this is a valid direction, so we can start following the loop
        map[start.y * 2 + next_move.y][start.x * 2 + next_move.x] = "X"
        next_direction = get_new_direction(next_pipe_direction, next_move)
        while True:
            # Record the location of the pipe
            map[next_square.y * 2][next_square.x * 2] = "P"

            # Record the movement between pipes
            map[next_square.y * 2 + next_direction.y][
                next_square.x * 2 + next_direction.x
            ] = "X"

            # Get the next square and direction
            next_square, next_direction = proceed_through_pipe(
                next_square, next_direction
            )

            # If there is no square to move into we're done
            if next_square is None:
                break

        # We only need to go around the loop in one direction
        # so we can stop now
        break


# Create a search queue starting with all the 'ground' spaces on
# the edges of the map

squares_queue = Queue()
for index in range(0, len(map[0])):
    if map[0][index] == ".":
        squares_queue.put(Coordinate(index, 0))
    if map[-1][index] == ".":
        squares_queue.put(Coordinate(index, len(map) - 1))
for index in range(0, len(map)):
    if map[index][0] == ".":
        squares_queue.put(Coordinate(0, index))
    if map[index][-1] == ".":
        squares_queue.put(Coordinate(len(map[0]) - 1, index))


# Search the entire map for ground outside the pipe loop
while True:
    try:
        square = squares_queue.get_nowait()
        value = map[square.y][square.x]
        if value != ".":
            # Already checked
            continue
        else:
            # This isn't a void, so mark it
            map[square.y][square.x] = "_"

            # Add all the adjacent unchecked squares to the queue
            squares_to_check = get_adjacent_ground_sqaures(square)
            for square in squares_to_check:
                squares_queue.put(square)

    except Empty:
        break

# Shrink the map back down to count the voids
new_map = [[" "] * (len(map[0]) // 2) for _ in range(len(map) // 2)]
for row in range(0, len(map), 2):
    for col in range(0, len(map[0]), 2):
        new_map[row // 2][col // 2] = map[row][col]

# Counting voids
void_count = 0
for row in new_map:
    for col in row:
        if col == ".":
            void_count += 1

print(void_count)
