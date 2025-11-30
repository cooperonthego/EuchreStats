import sqlite3

# Create (or open) the SQLite database
conn = sqlite3.connect("euchre.db")

# Enable foreign keys
conn.execute("PRAGMA foreign_keys = ON;")
cursor = conn.cursor()

# --- Create Player ---
cursor.execute("""
CREATE TABLE IF NOT EXISTS Player (
    id INTEGER PRIMARY KEY,
    name VARCHAR(50),
    displayName VARCHAR(50)
);
""")

# --- Create Game ---
cursor.execute("""
CREATE TABLE IF NOT EXISTS Game (
    id INTEGER PRIMARY KEY,
    gameStartTime DATETIME,
    gameEndTime DATETIME
);
""")

# --- Create Player_Game_Stats ---
cursor.execute("""
CREATE TABLE IF NOT EXISTS Player_Game_Stats (
    gameId INTEGER,
    playerId INTEGER,
    lonersWon INTEGER,
    lonersLost INTEGER,
    lonerEuchres INTEGER,
    PRIMARY KEY (gameId, playerId),
    FOREIGN KEY (gameId) REFERENCES Game(id) ON DELETE CASCADE,
    FOREIGN KEY (playerId) REFERENCES Player(id) ON DELETE CASCADE
);
""")

# --- Create Team_Game_Stats ---
cursor.execute("""
CREATE TABLE IF NOT EXISTS Team_Game_Stats (
    gameId INTEGER,
    playerId1 INTEGER,
    playerId2 INTEGER,
    won VARCHAR(1),
    numberEuchres INTEGER,
    PRIMARY KEY (gameId, playerId1, playerId2),
    FOREIGN KEY (gameId) REFERENCES Game(id) ON DELETE CASCADE,
    FOREIGN KEY (playerId1) REFERENCES Player(id) ON DELETE CASCADE,
    FOREIGN KEY (playerId2) REFERENCES Player(id) ON DELETE CASCADE
);
""")

conn.commit()
conn.close()

print("Database and tables created successfully!")
