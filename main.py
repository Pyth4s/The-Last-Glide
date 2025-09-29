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
portal_pairs = {'o': 'O', 'O': 'o', 'p': 'P', 'P': 'p', 'q': 'Q', 'Q': 'q'}
portal_links = {}

# Position von H und Ziel *
h_start = None
h_target = None
h_current_is_start = True

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
    print("Controls: w/a/s/d = move, r = reset, q = quit;\n"
          "'.' = Air, '#' = Wall, '+' = Box, '~' = Lava, 'S' = Slime Block, "
          "'%' = One-Time-Block, 'o/O/p/P/q/Q' = Portale, 'H' = beweglicher Block\n")
    for line in field:
        print(''.join(line))

def find_portal_target(x, y):
    return portal_links.get((x, y), None)

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
        if target in ['#', '+', 'H']:
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
            field[ny][nx] = '.'
            break
        if target in portal_pairs:
            dest = find_portal_target(nx, ny)
            if dest:
                cx, cy = dest
                continue
    field[cy][cx] = '+'
    return cx, cy

def load_level(level_number):
    global field, height, width, current_level, portal_links, h_start, h_target, h_current_is_start
    current_level = level_number
    field = [list(row) for row in original_levels[current_level]]
    height = len(field)
    width = len(field[0])
    portal_links = {}
    h_start = None
    h_target = None
    h_current_is_start = True

    portals = {}
    for y in range(height):
        for x in range(width):
            if field[y][x] in portal_pairs:
                symbol = field[y][x]
                pair_symbol = portal_pairs[symbol]
                portals.setdefault(symbol, (x, y))
                if pair_symbol in portals:
                    x2, y2 = portals[pair_symbol]
                    portal_links[(x, y)] = (x2, y2)
                    portal_links[(x2, y2)] = (x, y)
            if field[y][x] == 'H':
                h_start = (x, y)
            if field[y][x] == '*':
                h_target = (x, y)
                field[y][x] = '.'

def move_h_block():
    global h_current_is_start, h_start, h_target
    if not h_start or not h_target:
        return

    if h_current_is_start:
        src = h_start
        dst = h_target
    else:
        src = h_target
        dst = h_start

    sx, sy = src
    dx, dy = dst
    target = field[dy][dx]

    # Spieler treffen
    if target == '@':
        push_dx = dx - sx
        push_dy = dy - sy
        nx = dx + push_dx
        ny = dy + push_dy
        if 0 <= nx < width and 0 <= ny < height:
            next_target = field[ny][nx]
            if next_target in ['.', 'S']:
                field[sy][sx] = '.' if original_levels[current_level][sy][sx] != 'S' else 'S'
                field[dy][dx] = 'H'
                field[ny][nx] = '@'
                h_current_is_start = not h_current_is_start
            elif next_target in portal_pairs:
                dest = find_portal_target(nx, ny)
                if dest:
                    tx, ty = dest
                    field[sy][sx] = '.' if original_levels[current_level][sy][sx] != 'S' else 'S'
                    field[dy][dx] = 'H'
                    field[ty][tx] = '@'
                    h_current_is_start = not h_current_is_start
        return

    # Box treffen
    if target == '+':
        push_dx = dx - sx
        push_dy = dy - sy
        nx = dx + push_dx
        ny = dy + push_dy
        if 0 <= nx < width and 0 <= ny < height:
            next_target = field[ny][nx]
            if next_target in ['.', 'S']:
                field[ny][nx] = '+'
                field[dy][dx] = 'H'
                field[sy][sx] = '.' if original_levels[current_level][sy][sx] != 'S' else 'S'
                h_current_is_start = not h_current_is_start
            elif next_target in portal_pairs:
                dest = find_portal_target(nx, ny)
                if dest:
                    tx, ty = dest
                    field[ty][tx] = '+'
                    field[dy][dx] = 'H'
                    field[sy][sx] = '.' if original_levels[current_level][sy][sx] != 'S' else 'S'
                    h_current_is_start = not h_current_is_start
        return

    # normales Bewegen
    if target in ['.', 'S']:
        field[sy][sx] = '.' if original_levels[current_level][sy][sx] != 'S' else 'S'
        field[dy][dx] = 'H'
        h_current_is_start = not h_current_is_start

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
        if target == 'H':
            break
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
            move_h_block()
            return
        if target in portal_pairs:
            dest = find_portal_target(nx, ny)
            if dest:
                nx, ny = dest
        x, y = nx, ny
    place_player(x, y)
    move_h_block()

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
