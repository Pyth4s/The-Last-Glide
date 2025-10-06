import os

PROFILES_FILE = "profiles.txt"
LEVEL_COUNT = 35

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def parse_profiles():
    players = []
    if not os.path.exists(PROFILES_FILE):
        return players
    with open(PROFILES_FILE, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split(";")
            if len(parts) < 4:
                continue
            name, pwd, level_str, level_data = parts[0], parts[1], parts[2], parts[3]
            level_entries = level_data.split(",") if level_data else []
            stats = {}
            for entry in level_entries:
                if not entry.strip():
                    continue
                try:
                    lvl, time_val, moves, mps = entry.replace("lvl", "").split(":")
                    stats[int(lvl)] = {
                        "time": float(time_val),
                        "moves": int(moves),
                        "mps": float(mps)
                    }
                except ValueError:
                    continue
            try:
                level_int = int(level_str)
            except ValueError:
                level_int = 0
            players.append({
                "name": name,
                "level": level_int,
                "stats": stats
            })
    return players

def show_level_leaderboard(level_number):
    clear_screen()
    players = parse_profiles()
    ranking = []
    for p in players:
        if level_number in p["stats"]:
            s = p["stats"][level_number]
            ranking.append((p["name"], s["time"], s["moves"], s["mps"]))
    ranking.sort(key=lambda x: (x[1], x[2]))
    print(f"=== Rangliste für Level {level_number} ===")
    if not ranking:
        print("Keine Einträge für dieses Level.")
        print("\nDrücke Enter, um zurückzukehren...")
        input()
        return
    print(f"{'Platz':<6}{'Name':<15}{'Zeit (s)':<12}{'Moves':<10}{'MPS':<8}")
    print("-" * 60)
    for i, (name, time_s, moves, mps) in enumerate(ranking, start=1):
        print(f"{i:<6}{name:<15}{time_s:<12.3f}{moves:<10}{mps:<8.2f}")
    print("\nDrücke Enter, um zurückzukehren...")
    input()

def show_total_leaderboard():
    clear_screen()
    players = parse_profiles()
    ranking = []
    for p in players:
        if len(p["stats"]) >= LEVEL_COUNT:
            total_time = sum(s["time"] for s in p["stats"].values())
            total_moves = sum(s["moves"] for s in p["stats"].values())
            total_mps = total_moves / total_time if total_time > 0 else 0
            avg_time = total_time / LEVEL_COUNT
            ranking.append((p["name"], total_time, total_moves, avg_time, total_mps))
    ranking.sort(key=lambda x: x[1])
    print("=== Gesamtrangliste (alle Levels abgeschlossen) ===")
    if not ranking:
        print("Keine Spieler haben alle Levels abgeschlossen.")
        print("\nDrücke Enter, um zurückzukehren...")
        input()
        return
    print(f"{'Platz':<6}{'Name':<15}{'Gesamtzeit':<12}{'Moves':<10}{'Ø Zeit/Lvl':<12}{'MPS':<8}")
    print("-" * 80)
    for i, (name, total_time, moves, avg_time, mps) in enumerate(ranking, start=1):
        print(f"{i:<6}{name:<15}{total_time:<12.3f}{moves:<10}{avg_time:<12.3f}{mps:<8.2f}")
    print("\nDrücke Enter, um zurückzukehren...")
    input()

def show_menu():
    while True:
        clear_screen()
        print("=== Leaderboards ===")
        print("1) Level-Rangliste anzeigen")
        print("2) Gesamtrangliste (alle Levels)")
        print("Q) Zurück zum Hauptmenü")
        print("")
        choice = input("Auswahl: ").strip().lower()
        if choice == "1":
            while True:
                clear_screen()
                print("Wähle ein Level:")
                cols = 7
                line = ""
                for i in range(1, LEVEL_COUNT + 1):
                    entry = f"{i:>2}"
                    line += entry + ("  " if (i % cols) != 0 else "\n")
                if line and not line.endswith("\n"):
                    line += "\n"
                print(line)
                sel = input("Gib die Levelnummer ein oder 'B' zum Zurück: ").strip().lower()
                if sel == "b":
                    break
                try:
                    lvl = int(sel)
                    if 1 <= lvl <= LEVEL_COUNT:
                        show_level_leaderboard(lvl)
                    else:
                        print("Ungültige Levelnummer.")
                        input("Drücke Enter...")
                except ValueError:
                    print("Ungültige Eingabe.")
                    input("Drücke Enter...")
        elif choice == "2":
            show_total_leaderboard()
        elif choice == "q":
            break
        else:
            print("Ungültige Auswahl.")
            input("Drücke Enter...")
