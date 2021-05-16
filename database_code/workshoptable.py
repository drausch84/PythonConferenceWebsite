import sqlite3
import csv

with open('workshops.csv') as file:
    workshop_list = []

    reader = csv.reader(file)

    for row in reader:

        workshop = {'id': row[0], 'workshop_name': row[1], 'session': row[2], 'room_num': row[3], 'start_time': row[4],
                    'end_time': row[5]}

        workshop_list.append(workshop)

for key in workshop_list:
    print(key)

conn = sqlite3.connect("../conference.sqlite")

cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS workshops")

created_table = '''CREATE TABLE workshops(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    workshop_name TEXT,
    session INTEGER,
    room_num TEXT,
    start_time TEXT,
    end_time TEXT
    ) '''

cur.execute(created_table)
print("Table successfully created")

cur.executemany('''INSERT INTO workshops(id, workshop_name, session, room_num, start_time, end_time) VALUES 
(:id,:workshop_name,:session,:room_num,
:start_time,:end_time) ''', workshop_list)

conn.commit()

conn.close()