import csv

from flask import abort, flash, Flask, redirect, render_template, request, session, url_for
from flask_session import Session

app = Flask(__name__)

# Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def get_user(username):
    """ Returns username's row from csv file if it exists """

    with open("users.csv") as users_file:
        rows = csv.reader(users_file)
        for row in rows:
            if row[0] == username:
                return row


@app.route("/")
def index():
    return render_template("index.html", title="Homepage", username=session.get("username"))


@app.route("/register", methods=["GET", "POST"])
def register():
    # Ensure user is not logged in
    if session.get("username"):
        flash("must <a href='/logout'>logout</a> first")
        return redirect("/")

    # Handle GET requests
    if request.method == "GET":
        return render_template("register.html", title="Register")

    # Handle POST requests
    else:
        # Get username and password from form
        username = request.form.get("username")
        password = request.form.get("password")

        # Ensure username and password were submitted
        if not username or not password:
            abort(400, description="missing username or password")

        # Ensure username doesn't exist
        if get_user(username):
            abort(400, description="username already exists")

        # Register user
        with open("users.csv", mode="a") as users_file:
            users = csv.writer(users_file)
            users.writerow([username, password])

        # Remember user in session
        session["username"] = username

        # Redirect user back to index
        return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    # Handle GET requests
    if request.method == "GET":
        return render_template("login.html", title="Login")

    # Handle POST requests
    else:
        # Get username and password from form
        username = request.form.get("username")
        password = request.form.get("password")

        # Ensure username and password were submitted
        if not username or not password:
            abort(400, description="missing username or password")

        # Get user's row from csv
        user = get_user(username)

        # Ensure user was registered and password matches
        if user and user[1] == password:

            # Remember user in session
            session["username"] = username
            return redirect("/")

    abort(403, description="invalid username and/or password")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
