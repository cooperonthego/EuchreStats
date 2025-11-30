import sqlite3
from datetime import datetime, timedelta

conn = sqlite3.connect("euchre.db")
conn.execute("PRAGMA foreign_keys = ON;")
cur = conn.cursor()

# ------------------------------
# Insert Players
# ------------------------------
players = [
    ("Alice Smith", "Alice"),
    ("Bob Johnson", "Bob"),
    ("Charlie Brown", "Charlie"),
    ("Diana Evans", "Diana"),
    ("Evan Carter", "Evan")
]

cur.executemany("INSERT INTO Player (name, displayName) VALUES (?, ?);", players)

# ------------------------------
# Insert Games
# ------------------------------
now = datetime.now()
game1_start = now - timedelta(days=1)
game1_end = game1_start + timedelta(hours=1)

game2_start = now - timedelta(hours=2)
game2_end = game2_start + timedelta(hours=1)

games = [
    (game1_start.strftime("%Y-%m-%d %H:%M:%S"), game1_end.strftime("%Y-%m-%d %H:%M:%S")),
    (game2_start.strftime("%Y-%m-%d %H:%M:%S"), game2_end.strftime("%Y-%m-%d %H:%M:%S"))
]

cur.executemany("INSERT INTO Game (gameStartTime, gameEndTime) VALUES (?, ?);", games)

# ------------------------------
# Team Game Stats
# (Two teams of two players per game)
# ------------------------------
team_stats = [
    # Game 1
    (1, 1, 2, "Y", 1),   # Alice + Bob won
    (1, 3, 4, "N", 0),   # Charlie + Diana lost
    
    # Game 2
    (2, 1, 3, "N", 1),   # Alice + Charlie lost
    (2, 4, 5, "Y", 2)    # Diana + Evan won
]

cur.executemany("""
    INSERT INTO Team_Game_Stats 
    (gameId, playerId1, playerId2, won, numberEuchres)
    VALUES (?, ?, ?, ?, ?);
""", team_stats)

# ------------------------------
# Player Game Stats
# ------------------------------
player_stats = [
    # Game 1
    (1, 1, 1, 0, 0),  # Alice
    (1, 2, 0, 0, 0),  # Bob
    (1, 3, 0, 1, 0),  # Charlie
    (1, 4, 0, 0, 0),  # Diana

    # Game 2
    (2, 1, 0, 1, 0),  # Alice
    (2, 3, 1, 0, 0),  # Charlie
    (2, 4, 0, 0, 1),  # Diana
    (2, 5, 0, 0, 1)   # Evan
]

cur.executemany("""
    INSERT INTO Player_Game_Stats
    (gameId, playerId, lonersWon, lonersLost, lonerEuchres)
    VALUES (?, ?, ?, ?, ?);
""", player_stats)

conn.commit()
conn.close()

print("Sample data inserted successfully!")
