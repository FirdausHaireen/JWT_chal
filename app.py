from flask import Flask, render_template, request, send_from_directory

app = Flask(__name__)

users = {
    "admin": "supersneaky123"
}

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if users.get(username) == password:
            return render_template("flag.html")
        return "Login failed", 403
    return render_template("login.html")

@app.route("/robots.txt")
def robots():
    return app.send_static_file("robots.txt")

@app.route("/static/dev_notes/<path:filename>")
def dev_notes(filename):
    return send_from_directory("static/dev_notes", filename)
