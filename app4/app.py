import csv
import datetime

from flask import abort, flash, Flask, redirect, render_template, request, session, url_for
from flask_session import Session

app = Flask(__name__)

# Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def get_user(username):
    with open("users.csv") as users_file:
        rows = csv.reader(users_file)
        for row in rows:
            if row[0] == username:
                return row


def get_posts():
    with open("posts.csv") as posts_file:
        rows = csv.reader(posts_file)
        return [{"content": row[0], "author": row[1], "datetime": row[2]} for row in rows]

    return []


@app.route("/")
def index():
    return render_template("index.html", title="Homepage", username=session.get("username"), posts=get_posts())


@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get("username"):
        flash("must <a href='/logout'>logout</a> first")
        return redirect("/")

    if request.method == "GET":
        return render_template("register.html", title="Register")
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
    if request.method == "GET":
        return render_template("login.html", title="Login")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        if not username or not password:
            abort(400, description="missing username and/or password")

        user = get_user(username)
        if user and user[1] == password:
            session["username"] = username
            return redirect("/")

    abort(403, description="invalid username and/or password")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/post", methods=["POST"])
def post():
    content = request.form.get("content")
    author = session.get("username")
    if not content:
        abort(400, description="missing post content")
    elif not author:
        abort(403, description="must <a href='/login'>login</a> first")

    with open("posts.csv", mode="a") as posts_file:
        posts = csv.writer(posts_file)
        posts.writerow([content, author, str(datetime.datetime.now())])
        return redirect("/")
