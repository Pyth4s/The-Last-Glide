import os
import time
from time import sleep
from main import main_menu

PROFILES_FILE = "profiles.txt"
LEVELS_FILE = "levels.txt"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_levels(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read().strip()
    raw_levels = [block for block in content.split("\n\n") if block.strip()]
    levels = []
    for block in raw_levels:
        level = [list(line) for line in block.splitlines()]
        levels.append(level)
    return levels

levels = load_levels(LEVELS_FILE)
current_level = 0
original_levels = [[list(row) for row in level] for level in levels]

field = []
height = 0
width = 0

portal_pairs = {'o': 'O', 'O': 'o', 'p': 'P', 'P': 'p', 'q': 'Q', 'Q': 'q'}
portal_links = {}
h_blocks = []

def place_player(x, y):
    field[y][x] = '@'

def find_player():
    for yy in range(len(field)):
        for xx in range(len(field[yy])):
            if field[yy][xx] == '@':
                return xx, yy
    return None

def show_field():
    clear_screen()
    print(f"Level {current_level + 1} / {len(levels)}")
    print("Controls: w/a/s/d = move, r = reset, q = quit, Enter = move H blocks; b = back to main_menu\n"
          "'.' = Air, '#' = Wall, '+' = Box, '~' = Lava, 'S' = Slime Block, "
          "'%' = One-Time-Block, 'o/O/p/P/q/Q' = Portals, 'H' = moving Block, '*' = H-path\n")
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
    for yy in range(height):
        for xx in range(width):
            if field[yy][xx] == 'H' and (xx, yy) not in visited:
                path = []
                dfs(xx, yy, path)
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
        if (hx, hy) in path:
            field[hy][hx] = '*'
        else:
            field[hy][hx] = '.'
        if forward:
            idx += 1
            if idx >= len(path):
                idx = len(path) - 2 if len(path) >= 2 else 0
                block["forward"] = False
        else:
            idx -= 1
            if idx < 0:
                idx = 1 if len(path) >= 2 else 0
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
                field[ny][nx] = 'H'
            else:
                field[ny][nx] = 'H'
            continue
        if target == '+':
            dx = nx - hx
            dy = ny - hy
            bx, by = nx + dx, ny + dy
            if 0 <= bx < width and 0 <= by < height and field[by][bx] == '.':
                field[by][bx] = '+'
        field[ny][nx] = 'H'

player_name = None
level_start_time = None

def load_level(level_number: int):
    global field, height, width, current_level, portal_links, level_start_time
    current_level = level_number
    field = [list(row) for row in original_levels[current_level]]
    height = len(field)
    width = len(field[0]) if height > 0 else 0
    level_start_time = time.time()
    portal_links = {}
    portals = {}
    for yy in range(height):
        for xx in range(width):
            ch = field[yy][xx]
            if ch in portal_pairs:
                symbol = ch
                pair_symbol = portal_pairs[symbol]
                if symbol not in portals:
                    portals[symbol] = (xx, yy)
                if pair_symbol in portals:
                    x2, y2 = portals[pair_symbol]
                    portal_links[(xx, yy)] = (x2, y2)
                    portal_links[(x2, y2)] = (xx, yy)
    load_h_path()

def move(dx, dy):
    global current_level, level_start_time
    move_h_block()
    pos = find_player()
    if pos is None:
        return
    x, y = pos
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
            print("You fell into lava! Resetting level...")
            sleep(1)
            return
        if target == '+':
            push_box(nx, ny, dx, dy)
            place_player(x, y)
            return
        if target == 'H':
            break
        if target == 'X':
            elapsed = time.time() - level_start_time
            place_player(nx, ny)
            show_field()
            print(f"Level completed in {elapsed:.3f}s! Loading next level...")
            sleep(1)
            current_level += 1
            if player_name != "GUEST":
                try:
                    updated_lines = []
                    with open(PROFILES_FILE, "r", encoding="utf-8") as profile:
                        lines = profile.readlines()
                    for line in lines:
                        parts = line.strip().split(";")
                        if len(parts) < 3:
                            updated_lines.append(line)
                            continue
                        stored_user, stored_pass, stored_level = parts[:3]
                        stored_times = parts[3] if len(parts) > 3 else ""
                        if stored_user == player_name:
                            new_level = f"{stored_user};{stored_pass};{current_level + 1};"
                            if stored_times:
                                new_times = stored_times + f",lvl{current_level}:{elapsed:.3f}s"
                            else:
                                new_times = f"lvl{current_level}:{elapsed:.3f}s"
                            updated_lines.append(new_level + new_times + "\n")
                        else:
                            updated_lines.append(line)
                    with open(PROFILES_FILE, "w", encoding="utf-8") as profile:
                        profile.writelines(updated_lines)
                except FileNotFoundError:
                    print("Profiles file missing — cannot save progress.")
            if current_level >= len(levels):
                print("Congratulations! You finished all levels!")
                sleep(2)
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

def start_game(player: str):
    global current_level, player_name
    player_name = player
    current_level = 0
    if player_name != "GUEST":
        try:
            with open(PROFILES_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.strip().split(";")
                    if len(parts) < 3:
                        continue
                    stored_user, _, stored_level = parts[:3]
                    if stored_user == player_name:
                        try:
                            current_level = max(0, int(stored_level) - 1)
                        except ValueError:
                            current_level = 0
                        break
        except FileNotFoundError:
            pass
    load_level(current_level)
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
            sleep(1)
            break
        elif user_input == 'r':
            load_level(current_level)
            print("Level has been reset.")
            sleep(1)
        elif user_input == '':
            move_h_block()
        elif user_input == 'b':
            main_menu(player)
        elif user_input in direction_map:
            dx, dy = direction_map[user_input]
            move(dx, dy)
        else:
            print("Invalid input.")
            sleep(0.7)
