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

levels = load_levels("levels1.txt")
current_level = 0
original_levels = [[list(row) for row in level] for level in levels]
field = [list(row) for row in original_levels[current_level]]
height = len(field)
width = len(field[0])
portal_pairs = {'o': 'O', 'O': 'o', 'p': 'P', 'P': 'p', 'q': 'Q', 'Q': 'q'}
portal_links = {}
h_blocks = []

def place_player(x, y):
    field[y][x] = '@'

def find_player():
    for y in range(height):
        for x in range(width):
            if field[y][x] == '@':
                return x, y
    return None

def show_field():
    system('cls' if system.__name__ == 'system' else 'clear')
    print(f"Level {current_level + 1} / {len(levels)}")
    print("Controls: w/a/s/d = move, r = reset, q = quit, Enter = H bewegen;\n"
          "'.' = Air, '#' = Wall, '+' = Box, '~' = Lava, 'S' = Slime Block, "
          "'%' = One-Time-Block, 'o/O/p/P/q/Q' = Portale, 'H' = beweglicher Block, '*' = H-Pfad\n")
    for line in field:
        print(''.join(line))

def find_portal_target(x, y):
    return portal_links.get((x, y), None)

def push_box(x, y, dx, dy):
    cx, cy = x, y
    if original_levels[current_level][cy][cx] == 'S':
        field[cy][cx] = 'S'
    else:
        if any((cx, cy) in hb["path"] for hb in h_blocks):
            field[cy][cx] = '*'
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

def load_h_path():
    global h_blocks
    h_blocks = []
    visited = set()

    def dfs(x, y, path):
        if (x, y) in visited:
            return
        visited.add((x, y))
        path.append((x, y))
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height:
                if field[ny][nx] in ['*', 'H']:
                    dfs(nx, ny, path)

    for y in range(height):
        for x in range(width):
            if field[y][x] == 'H' and (x, y) not in visited:
                path = []
                dfs(x, y, path)
                if path:
                    h_blocks.append({
                        "path": path,
                        "index": 0,
                        "forward": True
                    })

def move_h_block():
    for block in h_blocks:
        path = block["path"]
        if not path:
            continue

        idx = block["index"]
        forward = block["forward"]

        hx, hy = path[idx]
        field[hy][hx] = '*' if (hx, hy) in path else '.'

        if forward:
            idx += 1
            if idx >= len(path):
                idx = len(path) - 2
                block["forward"] = False
        else:
            idx -= 1
            if idx < 0:
                idx = 1
                block["forward"] = True

        block["index"] = idx
        nx, ny = path[idx]
        target = field[ny][nx]

        if target == '@':
            dx = nx - hx
            dy = ny - hy
            px, py = nx + dx, ny + dy
            if 0 <= px < width and 0 <= py < height and field[py][px] == '.':
                field[py][px] = '@'

        if target == '+':
            dx = nx - hx
            dy = ny - hy
            bx, by = nx + dx, ny + dy
            if 0 <= bx < width and 0 <= by < height and field[by][bx] == '.':
                field[by][bx] = '+'

        field[ny][nx] = 'H'

def load_level(level_number):
    global field, height, width, current_level, portal_links
    current_level = level_number
    field = [list(row) for row in original_levels[current_level]]
    height = len(field)
    width = len(field[0])
    portal_links = {}
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
    load_h_path()

def move(dx, dy):
    global current_level, field, height, width
    move_h_block()
    x, y = find_player()
    if original_levels[current_level][y][x] == 'S':
        field[y][x] = 'S'
    else:
        if any((x, y) in hb["path"] for hb in h_blocks):
            field[y][x] = '*'
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
            return
        if target in portal_pairs:
            dest = find_portal_target(nx, ny)
            if dest:
                nx, ny = dest
        x, y = nx, ny
    place_player(x, y)

def start_game():
    direction_map = {
        'w': (0, -1),
        's': (0, 1),
        'a': (-1, 0),
        'd': (1, 0)
    }
    load_level(current_level)

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
        elif user_input == '':
            move_h_block()
        elif user_input in direction_map:
            dx, dy = direction_map[user_input]
            move(dx, dy)
        else:
            print("Invalid input.")
            sleep(1)
