import sqlite3

connection = sqlite3.connect("restaurant-20231203.db")

cursor = connection.cursor()

rows = cursor.execute("SELECT * FROM tables WHERE location = 'inside'").fetchall()
print(rows)
