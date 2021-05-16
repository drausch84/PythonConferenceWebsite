import sqlite3

conn = sqlite3.connect('../conference.sqlite')

cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS users")

created_table = '''CREATE TABLE users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT,
    first_name TEXT,
    last_name TEXT,
    password TEXT
    ) '''

cur.execute(created_table)
print("Table successfully created")

with open('users.csv', 'r') as file:
    num_records = 0
    for row in file:
        cur.execute("INSERT INTO users VALUES (?,?,?,?,?)", row.split(","))
        conn.commit()
        num_records += 1
conn.close()

print('\n{} Records Transferred'.format(num_records))
