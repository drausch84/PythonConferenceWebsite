import sqlite3
import csv
import pprint


class Registrant:
    def __init__(self, registration_date, title, first_name, last_name, street_address_1, street_address_2, city, state,
                 zip_code, phone_num, email, company_website, job_position, employer, meal_option, billing_first_name,
                 billing_last_name, credit_card_type, credit_card_num, security_code, exp_year, exp_month,
                 session_1_workshop, session_2_workshop, session_3_workshop):
        self.registration_date = registration_date
        self.title = title
        self.first_name = first_name
        self.last_name = last_name
        self.street_address_1 = street_address_1
        self.street_address_2 = street_address_2
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.phone_num = phone_num
        self.email = email
        self.company_website = company_website
        self.job_position = job_position
        self.employer = employer
        self.meal_option = meal_option
        self.billing_first_name = billing_first_name
        self.billing_last_name = billing_last_name
        self.credit_card_type = credit_card_type
        self.credit_card_num = credit_card_num
        self.security_code = security_code
        self.exp_year = exp_year
        self.exp_month = exp_month
        self.session_1_workshop = session_1_workshop
        self.session_2_workshop = session_2_workshop
        self.session_3_workshop = session_3_workshop


with open('registrant_data.csv', 'r') as file:
    registrant_list = []

    reader = csv.reader(file)

    for row in reader:
        registrant_list.append(Registrant(*row))


pprint.pprint(row)

conn = sqlite3.connect('../conference.sqlite')

cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS registration")

created_table = '''CREATE TABLE registration(
     id INTEGER PRIMARY KEY AUTOINCREMENT,
     registration_date TEXT,
     title TEXT,
     first_name TEXT,
     last_name TEXT,
     street_address_1 TEXT,
     street_address_2 TEXT,
     city TEXT,
     state TEXT,
     zip_code INTEGER,
     phone_num TEXT,
     email TEXT,
     company_website TEXT,
     job_position TEXT,
     employer TEXT,
     meal_option TEXT,
     billing_first_name TEXT,
     billing_last_name TEXT,
     credit_card_type TEXT,
     credit_card_num INTEGER,
     security_code INTEGER,
     exp_year INTEGER,
     exp_month INTEGER,
     session_1_workshop TEXT,
     session_2_workshop TEXT,
     session_3_workshop TEXT
     ) '''

cur.execute(created_table)
print("Table successfully created")

for registrant in registrant_list:
    reg_data = list(registrant.__dict__.values())
    cur.execute("INSERT INTO registration ('registration_date', 'title', 'first_name', 'last_name', "
                "'street_address_1','street_address_2', 'city', 'state', 'zip_code', 'phone_num', "
                "'email','company_website', 'job_position', 'employer', 'meal_option','billing_first_name', "
                "'billing_last_name', 'credit_card_type','credit_card_num', 'security_code', 'exp_year', "
                "'exp_month', 'session_1_workshop','session_2_workshop', 'session_3_workshop') "
                "VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", reg_data)

conn.commit()

conn.close()