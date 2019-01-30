import csv

from flask import abort, Flask, redirect, render_template, request, url_for

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", title="Homepage")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", title="Register")
    else:
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            abort(400, description="missing username or password")

        with open("users.csv") as users_file:
            rows = csv.reader(users_file)
            for row in rows:
                if row[0] == username:
                    abort(400, description="username already exists")

        with open("users.csv", mode="a") as users_file:
            users = csv.writer(users_file)
            users.writerow([username, password])

        return redirect("/")
