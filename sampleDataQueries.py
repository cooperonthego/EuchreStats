import sqlite3

conn = sqlite3.connect("euchre.db")
conn.execute("PRAGMA foreign_keys = ON;")
cur = conn.cursor()

# ---------------------------------------
# 1) Number of wins/losses for each player
# ---------------------------------------
print("\n1) Wins/Losses per Player")
cur.execute("""
SELECT 
    p.id,
    p.displayName,
    SUM(CASE WHEN tgs.won = 'Y' 
             AND (tgs.playerId1 = p.id OR tgs.playerId2 = p.id) THEN 1 ELSE 0 END) AS wins,
    SUM(CASE WHEN tgs.won = 'N' 
             AND (tgs.playerId1 = p.id OR tgs.playerId2 = p.id) THEN 1 ELSE 0 END) AS losses
FROM Player p
LEFT JOIN Team_Game_Stats tgs
    ON p.id IN (tgs.playerId1, tgs.playerId2)
GROUP BY p.id, p.displayName;
""")
print(cur.fetchall())


# ---------------------------------------
# 2) Number of wins/losses for each team
# (team defined by pair of players)
# ---------------------------------------
print("\n2) Wins/Losses per Team (with player names)")
cur.execute("""
SELECT 
    tgs.playerId1,
    p1.displayName AS player1Name,
    tgs.playerId2,
    p2.displayName AS player2Name,
    SUM(CASE WHEN tgs.won = 'Y' THEN 1 ELSE 0 END) AS wins,
    SUM(CASE WHEN tgs.won = 'N' THEN 1 ELSE 0 END) AS losses
FROM Team_Game_Stats tgs
JOIN Player p1 ON p1.id = tgs.playerId1
JOIN Player p2 ON p2.id = tgs.playerId2
GROUP BY 
    tgs.playerId1, 
    tgs.playerId2,
    p1.displayName,
    p2.displayName
ORDER BY wins DESC;
""")
print(cur.fetchall())



# ---------------------------------------
# 3) Number of Euchres for each game
# ---------------------------------------
print("\n3) Euchres per Game")
cur.execute("""
SELECT 
    gameId,
    SUM(numberEuchres) AS totalEuchres
FROM Team_Game_Stats
GROUP BY gameId;
""")
print(cur.fetchall())


# ---------------------------------------
# 4) Win percent for each player
# ---------------------------------------
print("\n4) Win Percent per Player")
cur.execute("""
WITH player_wins AS (
    SELECT 
        p.id AS playerId,
        SUM(CASE WHEN tgs.won = 'Y' 
                 AND p.id IN (tgs.playerId1, tgs.playerId2) THEN 1 ELSE 0 END) AS wins,
        SUM(CASE WHEN p.id IN (tgs.playerId1, tgs.playerId2) THEN 1 ELSE 0 END) AS gamesPlayed
    FROM Player p
    LEFT JOIN Team_Game_Stats tgs
        ON p.id IN (tgs.playerId1, tgs.playerId2)
    GROUP BY p.id
)
SELECT 
    playerId,
    (wins * 1.0 / gamesPlayed) AS winPercent
FROM player_wins;
""")
print(cur.fetchall())


# ---------------------------------------
# 5) Number of games played for each player
# ---------------------------------------
print("\n5) Games Played per Player")
cur.execute("""
SELECT 
    p.id,
    p.displayName,
    COUNT(tgs.gameId) AS gamesPlayed
FROM Player p
LEFT JOIN Team_Game_Stats tgs
    ON p.id IN (tgs.playerId1, tgs.playerId2)
GROUP BY p.id, p.displayName;
""")
print(cur.fetchall())


# ---------------------------------------
# 6) Number of games per team pair and win/loss ratio
# ---------------------------------------
print("\n6) Games + W/L Ratio per Team Pair (with player names)")
cur.execute("""
SELECT 
    tgs.playerId1,
    p1.displayName AS player1Name,
    tgs.playerId2,
    p2.displayName AS player2Name,
    COUNT(*) AS gamesPlayed,
    SUM(CASE WHEN tgs.won = 'Y' THEN 1 ELSE 0 END) AS wins,
    SUM(CASE WHEN tgs.won = 'N' THEN 1 ELSE 0 END) AS losses,
    (SUM(CASE WHEN tgs.won = 'Y' THEN 1 ELSE 0 END) * 1.0 / COUNT(*)) AS winRatio
FROM Team_Game_Stats tgs
JOIN Player p1 ON p1.id = tgs.playerId1
JOIN Player p2 ON p2.id = tgs.playerId2
GROUP BY 
    tgs.playerId1, 
    tgs.playerId2,
    p1.displayName,
    p2.displayName;
""")
print(cur.fetchall())


# ---------------------------------------
# 7) Number of Euchres per Player
# (sum of euchres their team achieved)
# ---------------------------------------
print("\n7) Euchres per Player")
cur.execute("""
SELECT 
    p.id,
    p.displayName,
    SUM(tgs.numberEuchres) AS euchres
FROM Player p
LEFT JOIN Team_Game_Stats tgs
    ON p.id IN (tgs.playerId1, tgs.playerId2)
GROUP BY p.id, p.displayName;
""")
print(cur.fetchall())


# ---------------------------------------
# 8) Loners won per Player
# ---------------------------------------
print("\n8) Loners Won per Player")
cur.execute("""
SELECT 
    p.id,
    p.displayName,
    SUM(pgs.lonersWon) AS lonersWon
FROM Player p
LEFT JOIN Player_Game_Stats pgs
    ON p.id = pgs.playerId
GROUP BY p.id, p.displayName;
""")
print(cur.fetchall())


# ---------------------------------------
# 9) Loners lost per Player
# ---------------------------------------
print("\n9) Loners Lost per Player")
cur.execute("""
SELECT 
    p.id,
    p.displayName,
    SUM(pgs.lonersLost) AS lonersLost
FROM Player p
LEFT JOIN Player_Game_Stats pgs
    ON p.id = pgs.playerId
GROUP BY p.id, p.displayName;
""")
print(cur.fetchall())


# ---------------------------------------
# 10) Loner euchres per Player
# ---------------------------------------
print("\n10) Loner Euchres per Player")
cur.execute("""
SELECT 
    p.id,
    p.displayName,
    SUM(pgs.lonerEuchres) AS lonerEuchres
FROM Player p
LEFT JOIN Player_Game_Stats pgs
    ON p.id = pgs.playerId
GROUP BY p.id, p.displayName;
""")
print(cur.fetchall())


conn.close()
