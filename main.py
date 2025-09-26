from os import system
from time import sleep

def load_levels(file):
    with open(file, "r", encoding="utf-8") as f:
        content = f.read().strip()

    raw_levels = content.split("\n\n")
    levels = []
    for block in raw_levels:
        level = [list(line) for line in block.splitlines()]
        levels.append(level)
    return levels

levels = load_levels("levels.txt")

current_level = 0
original_levels = [[list(row) for row in level] for level in levels]
field = [list(row) for row in original_levels[current_level]]

height = len(field)
width = len(field[0])

def place_player(x, y):
    field[y][x] = '@'

def find_player():
    for y in range(height):
        for x in range(width):
            if field[y][x] == '@':
                return x, y
    return None

def show_field():
    system('cls' if system.__name__ == 'posix' else 'clear')
    print(f"Level {current_level + 1} / {len(levels)}")
    print("Controls: w/a/s/d = move, r = reset, q = quit;\n'.' = Air, '#' = Wall, '+' = Box, '~' = Lava, 'S' = Slime Block, '%' = One-Time-Block\n")
    for line in field:
        print(''.join(line))

def push_box(x, y, dx, dy):
    cx, cy = x, y
    if original_levels[current_level][cy][cx] == 'S':
        field[cy][cx] = 'S'
    else:
        field[cy][cx] = '.'

    while True:
        nx = cx + dx
        ny = cy + dy

        if ny < 0 or ny >= height or nx < 0 or nx >= width:
            break

        target = field[ny][nx]

        if target in ['#', '+']:
            break
        if target == '~':
            field[ny][nx] = '.'
            return nx, ny
        if target == 'X':
            break
        if target == '.':
            cx, cy = nx, ny
            continue
        if target == 'S':
            cx, cy = nx, ny
            break
        if target == '%':
            original_levels[current_level][ny][nx] = '.'
            field[ny][nx] = '.'
            break

    field[cy][cx] = '+'
    return cx, cy

def load_level(level_number):
    global field, height, width, current_level
    current_level = level_number
    field = [list(row) for row in original_levels[current_level]]
    height = len(field)
    width = len(field[0])

def move(dx, dy):
    global current_level, field, height, width
    x, y = find_player()

    if original_levels[current_level][y][x] == 'S':
        field[y][x] = 'S'
    else:
        field[y][x] = '.'

    while True:
        nx = x + dx
        ny = y + dy

        if ny < 0 or ny >= height or nx < 0 or nx >= width:
            break
        
        target = field[ny][nx]

        if target == '#':
            break

        if target == '%':
            original_levels[current_level][ny][nx] = '.'
            field[ny][nx] = '.'
            break

        if target == '~':
            load_level(current_level)
            print("You fell into the lava! Resetting level...")
            sleep(1)
            return

        if target == '+':
            push_box(nx, ny, dx, dy)
            place_player(x, y)
            return

        if target == 'X':
            place_player(nx, ny)
            show_field()
            print("Level completed! Loading next level...")
            sleep(1)

            current_level += 1
            if current_level >= len(levels):
                print("Congratulations! You finished all levels!")
                exit(0)

            load_level(current_level)
            return

        if target == 'S':
            place_player(nx, ny)
            return

        x, y = nx, ny

    place_player(x, y)

direction_map = {
    'w': (0, -1),
    's': (0, 1),
    'a': (-1, 0),
    'd': (1, 0)
}

while True:
    show_field()
    user_input = input(": ").lower()

    if user_input == 'q':
        print("Game ended.")
        break
    elif user_input == 'r':
        load_level(current_level)
        print("Level has been reset.")
        sleep(1)
    elif user_input in direction_map:
        dx, dy = direction_map[user_input]
        move(dx, dy)
    else:
        print("Invalid input.")
        sleep(1)
