class Profile:
    tablename = "registration"
    COLUMNS = (
        "registration_date",
        "title",
        "first_name",
        "last_name",
        "street_address_1",
        "street_address_2",
        "city",
        "state",
        "zip_code",
        "phone_num",
        "email",
        "company_website",
        "job_position",
        "employer",
        "meal_option",
        "billing_first_name",
        "billing_last_name",
        "credit_card_type",
        "credit_card_num",
        "security_code",
        "exp_year",
        "exp_month",
        "session_1_workshop",
        "session_2_workshop",
        "session_3_workshop"
    )

    @staticmethod
    def insert_one(db, params):
        num_bindings = ",".join(["?" for column in Profile.COLUMNS])
        cols = ",".join(Profile.COLUMNS)
        sql = f"""INSERT INTO {Profile.tablename} ({cols}) VALUES ({num_bindings})"""
        cur = db.cursor()
        cur.execute(sql, params)
        db.commit()
        return cur.lastrowid