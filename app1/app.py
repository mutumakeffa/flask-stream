from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def index():
    # Get value of name GET parameter
    name = request.args.get("name")

    # Greet name
    return f"Hello, {name}!"
