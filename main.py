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

# Basis-Levels (statisch) einlesen
levels_base = load_levels("levels.txt")

# Startpositionen extrahieren: falls ein '@' in der Level-Datei ist,
# merken wir die Startposition und ersetzen '@' in der Basis durch '.'
start_positions = []
for li, lvl in enumerate(levels_base):
    found = None
    for y, row in enumerate(lvl):
        for x, ch in enumerate(row):
            if ch == '@':
                found = (x, y)
                levels_base[li][y][x] = '.'  # '@' gehört nicht zur statischen Karte
                break
        if found:
            break
    start_positions.append(found)

current_level = 0
# Dynamic map: veränderliche Kopie des aktuellen Level-Basis (Boxes, zerstörbare Blöcke, ...)
field = deepcopy(levels_base[current_level])

height = len(field)
width = len(field[0])

# Player-Position (wird nicht in 'field' geschrieben, nur zum Rendern überlagert)
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
    print("Legende: '.' = Air, '#' = Wall, '+' = Box, '~' = Lava, 'S' = Slime, '%' = One-Time, 'o'/'O' = Portal, 'X' = Ziel")
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
    # Prüft, ob der Spieler dort stehen kann (keine Wand, keine Box)
    if not in_bounds(x, y):
        return False
    if field[y][x] in ['#', '+']:
        return False
    return True

def teleport_destination_for(portal_char):
    # Finde das Gegenportal in der statischen Basis-Karte
    target_char = 'O' if portal_char == 'o' else 'o'
    for yy in range(height):
        for xx in range(width):
            if levels_base[current_level][yy][xx] == target_char:
                return (xx, yy)
    return None

def push_box(box_x, box_y, dx, dy):
    """
    Boxen gleiten wie im Originalcode bis zum Hindernis, mit ähnlichen Regeln:
    - Boxen stoppen bei '#' oder '+' oder 'X'
    - Boxen können nicht durch Portale ('o'/'O') geschoben werden
    - Wenn Box in Lava '~' geschoben wird -> Lava wird gelöscht (wie vorher)
    - Wenn Box auf '%' geschoben wird -> '%' wird entfernt und Box stoppt davor
    Rückgabe: (new_box_x, new_box_y) oder None wenn Push nicht möglich
    """
    cx, cy = box_x, box_y
    # setze die Ursprungszelle zurück auf die Basis (Box verschiebt sich)
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
            # Box fällt in Lava -> Lava wird entfernt
            field[ny][nx] = '.'
            return (nx, ny)
        if target == '.':
            cx, cy = nx, ny
            continue
        if target == 'S':
            # Slime stoppt die Box
            cx, cy = nx, ny
            break
        if target == '%':
            # one-time block wird zerstört; Box stoppt davor (wie vorher)
            levels_base[current_level][ny][nx] = '.'
            field[ny][nx] = '.'
            break
        if target in ['o', 'O']:
            # Boxen dürfen nicht durch Portale
            break

    field[cy][cx] = '+'
    return (cx, cy)

def move(dx, dy):
    """
    Rutschbewegung: Der Spieler bewegt sich solange in (dx,dy) weiter,
    bis er auf einen Stopp-Fall trifft (wie im Original).
    """
    global player_pos, field, current_level
    x, y = player_pos

    # Wir simulieren Schritt-für-Schritt in der Bewegungsrichtung.
    while True:
        nx = x + dx
        ny = y + dy

        # außerhalb
        if not in_bounds(nx, ny):
            break

        target = field[ny][nx]
        base_tile = levels_base[current_level][ny][nx]

        # Wand -> stoppe; Spieler bleibt auf x,y
        if target == '#':
            break

        # One-time block: zerstöre und stoppe; Spieler bleibt auf x,y (wie original)
        if target == '%':
            levels_base[current_level][ny][nx] = '.'
            field[ny][nx] = '.'
            break

        # Lava -> Reset direkt
        if target == '~':
            load_level(current_level)
            print("You fell into the lava! Resetting level...")
            sleep(1)
            return

        # Box: versuche zu schieben; wenn geschoben wird, Bewegung stoppt (Spieler bleibt auf x,y)
        if target == '+':
            res = push_box(nx, ny, dx, dy)
            # falls push_box etwas getan hat, bleibt der Spieler vor der Kiste (wie vorher)
            return

        # Ziel-Feld -> setze Spieler auf Ziel und lade nächstes Level
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

        # Slime: betrete Slime und stoppe (wie original)
        if target == 'S':
            player_pos = (nx, ny)
            return

        # Portal betreten: benutze die Basis-Karte zur Erkennung
        if base_tile in ['o', 'O']:
            dest = teleport_destination_for(base_tile)
            if dest:
                tx, ty = dest
                # teleport nur, wenn Ziel frei ist (keine Wand/Box)
                if can_occupy(tx, ty):
                    # Teleportiere den Spieler auf das Gegenportal und setze x,y dorthin
                    x, y = tx, ty
                    # setzte loop fort -> rutscht weiter ab Zielportal
                    continue
                else:
                    # Ziel blockiert -> Spieler bleibt auf dem betretenen Portal
                    player_pos = (nx, ny)
                    return
            else:
                # kein Gegenportal -> steh einfach auf dem Portal
                player_pos = (nx, ny)
                return

        # Normale Luft: bewege Spieler weiter (rutschen)
        if target == '.':
            x, y = nx, ny
            # weiter in der Schleife: rutschen bis stop
            continue

        # Sonstige Fälle (falls noch welche): blockieren
        break

    # Schleife beendet -> setze Spieler an letzte Position x,y
    player_pos = (x, y)

direction_map = {
    'w': (0, -1),
    's': (0, 1),
    'a': (-1, 0),
    'd': (1, 0)
}

# Initiale Absicherung: wenn keine Startpos gesetzt wurde, finde eine leere Zelle
if player_pos is None:
    player_pos = find_first_free()

# Spielschleife
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
