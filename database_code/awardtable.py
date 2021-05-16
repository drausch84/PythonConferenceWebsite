import sqlite3

conn = sqlite3.connect("../conference.sqlite")

cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS nominees")

created_table = '''CREATE TABLE nominees(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nominee_name TEXT,
    description TEXT,
    image_name TEXT,
    current_votes INTEGER
    ) '''

cur.execute(created_table)
print("Table successfully created")

with open('awards.csv', 'r') as file:
    num_records = 0
    for row in file:
        cur.execute("INSERT INTO nominees VALUES (?,?,?,?,?)", row.split(","))
        conn.commit()
        num_records += 1

conn.close()

print('\n{} Records Transferred'.format(num_records))