from os import system
from time import sleep

levels = [
    [
        list("########"),
        list("#.......#"),
        list("##......#"),
        list("#.....#.#"),
        list("#@......#"),
        list("#####X##")
    ],
    [
        list("#########"),
        list("##.....##"),
        list("#..#....#"),
        list("#..#..X.#"),
        list("#@....#.#"),
        list("#########")
    ],
    [
        list("#########"),
        list("#...#...#"),
        list("#...#...#"),
        list("#...#..X#"),
        list("#@......#"),
        list("#########")
    ],
    [
        list("##X######"),
        list("##.....##"),
        list("#....#..#"),
        list("#..#....#"),
        list("#@...#..#"),
        list("#########")
    ],
    [
        list("#########"),
        list("#.#...#.#"),
        list("#......##"),
        list("#..#X...#"),
        list("#@.##...#"),
        list("#########")
    ],
    [
        list("###########"),
        list("#.........#"),
        list("#......#..#"),
        list("#.....X...#"),
        list("#.+.......#"),
        list("#.@.......#"),
        list("###########")
    ],
    [
        list("###########"),
        list("#.........#"),
        list("#.........#"),
        list("#.....X...#"),
        list("#.+..#...+#"),
        list("#.@.......#"),
        list("###########")
    ],
    [
        list("###########"),
        list("#...#.....#"),
        list("#.#......##"),
        list("#.....X.+.#"),
        list("#.+.......#"),
        list("#.@..#....#"),
        list("###########")
    ],
    [
        list("###########"),
        list("#.+......##"),
        list("#.........#"),
        list("#....X....#"),
        list("#......+..#"),
        list("#.@.....#.#"),
        list("###########")
    ],
    [
        list("###########"),
        list("#........##"),
        list("#.+.......#"),
        list("##...#....X"),
        list("#....+....#"),
        list("#.@.......#"),
        list("###########")
    ],
    [
        list("###########"),
        list("#.........#"),
        list("#.#.......#"),
        list("#........~X"),
        list("#........+#"),
        list("##@.......#"),
        list("###########")
    ],
    [
        list("###########"),
        list("#........##"),
        list("#...+....##"),
        list("#...#~~~~.X"),
        list("#+......+##"),
        list("#.@......##"),
        list("###########")
    ],
    [
        list("###########"),
        list("#.........#"),
        list("##..@....##"),
        list("#~.+~X..+.#"),
        list("#+~~#...~##"),
        list("#.........#"),
        list("###########")
    ],
    [
        list("###########"),
        list("#..#.....@#"),
        list("#.~~+.~~~.#"),
        list("#........+#"),
        list("##..~~..+~#"),
        list("##X#.....##"),
        list("###########")
    ],
    [
        list("###########"),
        list("##~~..~.+~#"),
        list("#.++....#.#"),
        list("#~~@....~.#"),
        list("#~X+..++.+#"),
        list("#~~~...+.~#"),
        list("###########")
    ],
    [
        list("###########"),
        list("#~~~~.....#"),
        list("#.S..S~XS.#"),
        list("#.........#"),
        list("#......#..#"),
        list("#.@....~.##"),
        list("###########")
    ],
    [
        list("###########"),
        list("#.S.....#.#"),
        list("#.+S......#"),
        list("##...@.+#.#"),
        list("#~.....S..#"),
        list("#X~..#.#..#"),
        list("###########")
    ],
        [
        list("###########"),
        list("#~....+.~##"),
        list("#@...S..+.#"),
        list("#........##"),
        list("#....S....#"),
        list("#~...~....#"),
        list("#####X#####")
    ],
    [
        list("###########"),
        list("#@.......##"),
        list("#...~..~+.#"),
        list("#..~X.~S~.#"),
        list("#...~.+~.+#"),
        list("#.....S...#"),
        list("###########")
    ],
    [
        list("###########"),
        list("#@.~..S.S.#"),
        list("#.S.~.+S.+#"),
        list("#....X~S.~#"),
        list("#.S++...S~#"),
        list("#..SS.....#"),
        list("###########")
    ],
]

aktuelle_level = 0
urspruengliches_level = [[list(reihe) for reihe in level] for level in levels]
spielfeld = [list(reihe) for reihe in urspruengliches_level[aktuelle_level]]

hoehe = len(spielfeld)
breite = len(spielfeld[0])

def setze_spieler(x, y):
    spielfeld[y][x] = '@'

def finde_spieler():
    for y in range(hoehe):
        for x in range(breite):
            if spielfeld[y][x] == '@':
                return x, y
    return None

def zeige_spielfeld():
    system('cls' if system.__name__ == 'posix' else 'clear')
    print(f"Level {aktuelle_level + 1} / {len(levels)}")
    print("Steuerung: w/a/s/d = bewegen, r = reset, q = beenden\n")
    for zeile in spielfeld:
        print(''.join(zeile))

def kann_schieben(x, y, dx, dy):
    nx = x + dx
    ny = y + dy
    if 0 <= nx < breite and 0 <= ny < hoehe:
        ziel = spielfeld[ny][nx]
        if ziel == '#' or ziel == '+':
            return False
        return True
    return False

def schiebe_plus(x, y, dx, dy):
    cx, cy = x, y
    spielfeld[cy][cx] = '.'  

    while True:
        nx = cx + dx
        ny = cy + dy

        if ny < 0 or ny >= hoehe or nx < 0 or nx >= breite:
            break

        ziel = spielfeld[ny][nx]

        if ziel == '#':
            break
        if ziel == '+':
            break
        if ziel == '~':
            spielfeld[ny][nx] = '.'
            return nx, ny
        if ziel == 'X':
            break
        if ziel == '.':
            cx, cy = nx, ny
            continue

    spielfeld[cy][cx] = '+'
    return cx, cy

def lade_level(level_nummer):
    global spielfeld, hoehe, breite, aktuelle_level
    aktuelle_level = level_nummer
    spielfeld = [list(reihe) for reihe in urspruengliches_level[aktuelle_level]]
    hoehe = len(spielfeld)
    breite = len(spielfeld[0])

def bewege(dx, dy):
    global aktuelle_level, spielfeld, hoehe, breite
    x, y = finde_spieler()

    if urspruengliches_level[aktuelle_level][y][x] == 'S':
        spielfeld[y][x] = 'S'
    else:
        spielfeld[y][x] = '.'

    while True:
        nx = x + dx
        ny = y + dy

        if ny < 0 or ny >= hoehe or nx < 0 or nx >= breite:
            break
        
        ziel = spielfeld[ny][nx]

        if ziel == '#':
            break

        if ziel == '~':
            lade_level(aktuelle_level)
            print("Du bist in die Lava gefallen! Level wird zurückgesetzt...")
            sleep(1)
            return

        if ziel == '+':
            schiebe_plus(nx, ny, dx, dy)
            setze_spieler(x, y)
            return

        if ziel == 'X':
            setze_spieler(nx, ny)
            zeige_spielfeld()
            print("Level geschafft! Lade nächstes Level...")
            sleep(1)

            aktuelle_level += 1
            if aktuelle_level >= len(levels):
                print("Herzlichen Glückwunsch! Du hast alle Levels geschafft!")
                exit(0)

            lade_level(aktuelle_level)
            return

        if ziel == 'S':
            setze_spieler(nx, ny)
            return

        x, y = nx, ny

    setze_spieler(x, y)

richtung_map = {
    'w': (0, -1),
    's': (0, 1),
    'a': (-1, 0),
    'd': (1, 0)
}

while True:
    zeige_spielfeld()
    eingabe = input(": ").lower()

    if eingabe == 'q':
        print("Spiel beendet.")
        break
    elif eingabe == 'r':
        lade_level(aktuelle_level)
        print("Level wurde zurückgesetzt.")
        sleep(1)
    elif eingabe in richtung_map:
        dx, dy = richtung_map[eingabe]
        bewege(dx, dy)
    else:
        print("Ungültige Eingabe.")
        sleep(1)

# lever
# sticky block -> man bleibt drauf stehen
# 1 time block -> verschwindet bei berührung
# bewegliche -> jede bewegung bewegen sie sich
# teleportation blocke