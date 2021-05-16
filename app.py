import sqlite3

from flask import Flask, render_template, request, session, redirect
from functools import wraps
from database_code.Profile import Profile

app = Flask(__name__)


def db_connect():
    db_name = "conference.sqlite"
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    return conn


def status(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'logged_in' in session:
            return func(*args, **kwargs)
        return "You Are Not Logged In"
    return wrapper


@app.route('/')
def home():
    logged_in = session['logged_in']
    return render_template("index.html", logged_in=logged_in)


@app.route('/activities')
def activities():
    logged_in = session['logged_in']
    return render_template("activities.html", logged_in=logged_in)


@app.route('/awards', methods=['GET', 'POST'])
def awards():
    logged_in = session['logged_in']
    thxmsg = "Thank You For Voting"
    if request.method == 'GET':
        return render_template("awards.html", logged_in=logged_in)
    else:
        return render_template("awards.html", thankyoumsg=thxmsg, logged_in=logged_in)


@app.route('/keynote')
def keynote():
    logged_in = session['logged_in']
    return render_template("keynote.html", logged_in=logged_in)


@app.route('/meals')
def meals():
    logged_in = session['logged_in']
    return render_template("meals.html", logged_in=logged_in)


@app.route('/workshop')
def workshop():
    logged_in = session['logged_in']
    return render_template("workshopschedule.html", logged_in=logged_in)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    logged_in = session['logged_in']
    if request.method == 'POST':
        profile = {}
        try:
            title = request.form.get('nameTitle')
            firstName = request.form.get('firstName')
            lastName = request.form.get('lastName')
            streetAddress = request.form.get('streetAddress')
            streetAddress2 = request.form.get('streetAddress2')
            city = request.form.get('city')
            states = request.form.get('states')
            zipcode = request.form.get('zipcode')
            phone = request.form.get('phone')
            email = request.form.get('email')
            employer = request.form.get('employer')
            website = request.form.get('website')
            job_pos = request.form.get('job-pos')
            session_one_choice = request.form.get('session-one-choice')
            session_two_choice = request.form.get('session-two-choice')
            session_three_choice = request.form.get('session-three-choice')
            params = ["NULL", title, firstName, lastName, streetAddress, streetAddress2, city, states, zipcode, phone,
                      email, website, job_pos, employer, "NULL", "NULL", "NULL", "NULL", 0, 0, 0, 0, session_one_choice,
                      session_two_choice, session_three_choice]
            print(params)
            with db_connect() as db:
                rowid = Profile.insert_one(db, params)
                print(rowid)
                cur = db.cursor()
                profile_data = cur.execute("SELECT * from registration WHERE id=?", (rowid,)).fetchone()
                cols = [column for column in Profile.COLUMNS]
                for column, data in zip(["id"]+cols, profile_data):
                    profile[column] = data
                print(profile)
                db.close()
        except ImportError:
            print("ERROR!!!!")
        except:
            db.rollback()
        finally:
            return render_template("thankyou.html", **profile, logged_in=logged_in)
    else:
        return render_template("registration.html", logged_in=logged_in)


@app.route('/admin')
@status
def admin():
    logged_in = session['logged_in']
    return render_template('admin.html', logged_in=logged_in)


@app.route('/nametags8')
def nametags8():
    return render_template('nametags8.html')


@app.route('/nametags10')
def nametags10():
    return render_template('nametags10.html')


@app.route('/lists', methods=['GET', 'POST'])
@status
def lists():
    logged_in = session['logged_in']
    with db_connect() as db:
        db.row_factory = sqlite3.Row
        cur = db.cursor()
        if request.method == 'POST':
            if request.form['registrant-choice'] == 'full-registrant-list':
                cur.execute("SELECT * from registration")
                registrant_list = cur.fetchall()
                list_h = "Full Registrant List"
                return render_template('lists.html', registrant_list=registrant_list, list_h=list_h)
            elif request.form['registrant-choice'] == 'successful-short-story':
                cur.execute("SELECT first_name, last_name from registration where session_1_workshop = 'Workshop A' OR "
                            "session_1_workshop = 'successful-short-story'")
                registrant_list = cur.fetchall()
                list_h = "Short Story Workshop Registrants"
                return render_template('lists.html', registrant_list=registrant_list, list_h=list_h)
            elif request.form['registrant-choice'] == 'descriptive-settings':
                cur.execute("SELECT first_name, last_name from registration where session_1_workshop = 'Workshop B' OR "
                            "session_1_workshop = 'descriptive-settings'")
                registrant_list = cur.fetchall()
                list_h = "Descriptive Settings Workshop Registrants"
                return render_template('lists.html', registrant_list=registrant_list, list_h=list_h)
            elif request.form['registrant-choice'] == 'resolution-conflict':
                cur.execute("SELECT first_name, last_name from registration where session_1_workshop = 'Workshop C' OR "
                            "session_1_workshop = 'resolution-conflict'")
                registrant_list = cur.fetchall()
                list_h = "Resolution and Conflict Workshop Registrants"
                return render_template('lists.html', registrant_list=registrant_list, list_h=list_h)
            elif request.form['registrant-choice'] == 'comedy-writing':
                cur.execute("SELECT first_name, last_name from registration where session_2_workshop = 'Workshop D' OR "
                            "session_2_workshop = 'comedy-writing'")
                registrant_list = cur.fetchall()
                list_h = "Comedy Writing Workshop Registrants"
                return render_template('lists.html', registrant_list=registrant_list, list_h=list_h)
            elif request.form['registrant-choice'] == 'poetry-writing':
                cur.execute("SELECT first_name, last_name from registration where session_2_workshop = 'Workshop E' OR "
                            "session_2_workshop = 'poetry-writing'")
                registrant_list = cur.fetchall()
                list_h = "Poetry Writing Workshop Registrants"
                return render_template('lists.html', registrant_list=registrant_list, list_h=list_h)
            elif request.form['registrant-choice'] == 'char-development':
                cur.execute("SELECT first_name, last_name from registration where session_2_workshop = 'Workshop F' OR "
                            "session_2_workshop = 'char-development'")
                registrant_list = cur.fetchall()
                list_h = "Character Development Workshop Registrants"
                return render_template('lists.html', registrant_list=registrant_list, list_h=list_h)
            elif request.form['registrant-choice'] == 'fiction-writing':
                cur.execute("SELECT first_name, last_name from registration where session_3_workshop = 'Workshop G' OR "
                            "session_3_workshop = 'fiction-writing'")
                registrant_list = cur.fetchall()
                list_h = "Fiction Writing Workshop Registrants"
                return render_template('lists.html', registrant_list=registrant_list, list_h=list_h)
            elif request.form['registrant-choice'] == 'plot-structure':
                cur.execute("SELECT first_name, last_name from registration where session_3_workshop = 'Workshop H' OR "
                            "session_3_workshop ='plot-structure'")
                registrant_list = cur.fetchall()
                list_h = "Plot and Structure Workshop Registrants"
                return render_template('lists.html', registrant_list=registrant_list, list_h=list_h)
            elif request.form['registrant-choice'] == 'mystery-novel':
                cur.execute("SELECT first_name, last_name from registration where session_3_workshop = 'Workshop I' OR "
                            "session_3_workshop = 'mystery-novel'")
                registrant_list = cur.fetchall()
                list_h = "Mystery Novel Workshop Registrants"
                return render_template('lists.html', registrant_list=registrant_list, list_h=list_h)
            elif request.form['registrant-choice'] == 'mealpack':
                cur.execute("SELECT first_name, last_name from registration where meal_option LIKE 'mealpack'")
                registrant_list = cur.fetchall()
                list_h = "Meal Pack Registrants"
                return render_template('lists.html', registrant_list=registrant_list, list_h=list_h)
            elif request.form['registrant-choice'] == 'day-2-dinner':
                cur.execute("SELECT first_name, last_name from registration where meal_option LIKE 'dinnerday2'")
                registrant_list = cur.fetchall()
                list_h = "Day 2 Dinner Registrants"
                return render_template('lists.html', registrant_list=registrant_list, list_h=list_h)
        else:
            return render_template('lists.html', logged_in=logged_in)


@app.route('/login', methods=['GET', 'POST'])
@status
def login():
    logged_in = session['logged_in']
    if request.method == 'POST':
        session.pop('user', None)
        if request.form['username'] == 'drausch':
            if request.form['password'] == 'fakepassword':
                session['logged_in'] = True
                return render_template('admin.html', logged_in=logged_in)
        elif request.form['username'] == 'lsmalls':
            if request.form['password'] == 'justapw':
                session['logged_in'] = True
                return render_template('admin.html', logged_in=logged_in)
        elif request.form['username'] == 'mbarrett':
            if request.form['password'] == 'nopenotno':
                session['logged_in'] = True
                return render_template('admin.html', logged_in=logged_in)
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['logged_in'] = False
    return redirect('/login')


app.secret_key = 'TheOhioStateBuckeyesAreMyFavoriteTeam'


if __name__ == '__main__':
    app.run(debug=True)