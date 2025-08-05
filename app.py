from flask import Flask, request, jsonify, render_template
import jwt
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'

users = {
    "user": {"password": "userpass", "is_admin": False},
    "admin": {"password": "adminpass", "is_admin": True}  # not for direct login
}

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = users.get(username)
        if user and user["password"] == password:
            token = jwt.encode({
                "username": username,
                "is_admin": user["is_admin"],
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            }, app.config["SECRET_KEY"], algorithm="HS256")
            return render_template("token.html", token=token)
        return "Invalid credentials", 403
    return render_template("login.html")

@app.route("/admin")
def admin():
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return "Missing or invalid token", 401

    token = auth_header.split(" ")[1]
    try:
        decoded = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256", "none"])
    except jwt.exceptions.InvalidTokenError:
        return "Invalid token", 403

    if decoded.get("is_admin") == True:
        return jsonify({"flag": "FLAG{jwt_none_alg_attack_success}"})
    return "Admins only!", 403
