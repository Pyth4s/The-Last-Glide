from os import system
from time import sleep
from copy import deepcopy

def load_levels(file):
    with open(file, "r", encoding="utf-8") as f:
        content = f.read().rstrip("\n")
    raw_levels = content.split("\n\n")
    levels = []
    for block in raw_levels:
        level = [list(line) for line in block.splitlines()]
        levels.append(level)
    return levels

levels_base = load_levels("levels.txt")

start_positions = []
for li, lvl in enumerate(levels_base):
    found = None
    for y, row in enumerate(lvl):
        for x, ch in enumerate(row):
            if ch == '@':
                found = (x, y)
                levels_base[li][y][x] = '.'
                break
        if found:
            break
    start_positions.append(found)

current_level = 0
field = deepcopy(levels_base[current_level])

height = len(field)
width = len(field[0])

player_pos = start_positions[current_level] or (0, 0)

def load_level(level_number):
    global field, height, width, current_level, player_pos
    current_level = level_number
    field = deepcopy(levels_base[current_level])
    height = len(field)
    width = len(field[0])
    player_pos = start_positions[current_level] or find_first_free()

def find_first_free():
    for y in range(height):
        for x in range(width):
            if field[y][x] == '.':
                return (x, y)
    return (0, 0)

def show_field():
    system('cls' if system.__name__ == 'posix' else 'clear')
    print(f"Level {current_level + 1} / {len(levels_base)}")
    print("Controls: w/a/s/d = move, r = reset, q = quit")
    print("Legende: '.' = Air, '#' = Wall, '+' = Box, '~' = Lava, 'S' = Slime, '%' = One-Time, 'o'/'O' = Portal, 'q'/'Q' = Portal, 'p'/'P' = Portal, 'X' = Ziel")
    for y in range(height):
        line = ""
        for x in range(width):
            if (x, y) == player_pos:
                line += '@'
            else:
                line += field[y][x]
        print(line)

def in_bounds(x, y):
    return 0 <= x < width and 0 <= y < height

def can_occupy(x, y):
    if not in_bounds(x, y):
        return False
    if field[y][x] in ['#', '+']:
        return False
    return True

def teleport_destination_for(portal_char):
    # Unterstützt jetzt: o/O, q/Q, p/P (all paarweise: lower<->upper)
    target_char = portal_char.upper() if portal_char.islower() else portal_char.lower()
    for yy in range(height):
        for xx in range(width):
            if levels_base[current_level][yy][xx] == target_char:
                return (xx, yy)
    return None

def push_box(box_x, box_y, dx, dy):
    cx, cy = box_x, box_y
    field[cy][cx] = levels_base[current_level][cy][cx]

    while True:
        nx = cx + dx
        ny = cy + dy

        if not in_bounds(nx, ny):
            break

        target = field[ny][nx]

        if target in ['#', '+', 'X']:
            break
        if target == '~':
            field[ny][nx] = '.'
            return (nx, ny)
        if target == '.':
            cx, cy = nx, ny
            continue
        if target == 'S':
            cx, cy = nx, ny
            break
        if target == '%':
            levels_base[current_level][ny][nx] = '.'
            field[ny][nx] = '.'
            break
        if target in ['o', 'O', 'q', 'Q', 'p', 'P']:
            # Box trifft ein Portal: aktuell wird es wie ein Hindernis behandelt
            break

    field[cy][cx] = '+'
    return (cx, cy)

def move(dx, dy):
    global player_pos, field, current_level
    x, y = player_pos

    while True:
        nx = x + dx
        ny = y + dy

        if not in_bounds(nx, ny):
            break

        target = field[ny][nx]
        base_tile = levels_base[current_level][ny][nx]

        if target == '#':
            break

        if target == '%':
            levels_base[current_level][ny][nx] = '.'
            field[ny][nx] = '.'
            break

        if target == '~':
            load_level(current_level)
            print("You fell into the lava! Resetting level...")
            sleep(1)
            return

        if target == '+':
            res = push_box(nx, ny, dx, dy)
            return

        if target == 'X':
            player_pos = (nx, ny)
            show_field()
            print("Level completed! Loading next level...")
            sleep(1)
            current_level += 1
            if current_level >= len(levels_base):
                print("Congratulations! You finished all levels!")
                exit(0)
            load_level(current_level)
            return

        if target == 'S':
            player_pos = (nx, ny)
            return

        # Unterstütze Teleport-Paare o/O, q/Q, p/P
        if base_tile in ['o', 'O', 'q', 'Q', 'p', 'P']:
            dest = teleport_destination_for(base_tile)
            if dest:
                tx, ty = dest
                if can_occupy(tx, ty):
                    x, y = tx, ty
                    continue
                else:
                    player_pos = (nx, ny)
                    return
            else:
                player_pos = (nx, ny)
                return

        if target == '.':
            x, y = nx, ny
            continue

        break

    player_pos = (x, y)

direction_map = {
    'w': (0, -1),
    's': (0, 1),
    'a': (-1, 0),
    'd': (1, 0)
}

if player_pos is None:
    player_pos = find_first_free()

while True:
    show_field()
    user_input = input(": ").lower().strip()
    if user_input == 'q':
        print("Game ended.")
        break
    if user_input == 'r':
        load_level(current_level)
        print("Level has been reset.")
        sleep(1)
        continue
    if user_input in direction_map:
        dx, dy = direction_map[user_input]
        move(dx, dy)
        continue
    print("Invalid input.")
    sleep(0.6)
