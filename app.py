# app.py

from flask import Flask, render_template, request, redirect, url_for, session
import re

app = Flask(__name__)
app.secret_key = "your_secret_key_here"

# -------------------- HOME --------------------
@app.route("/")
def home():
    return render_template("login.html")

# -------------------- LOGIN --------------------
@app.route("/login", methods=["POST"])
def login():
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    password = request.form.get("password")

    # Backend validation
    if not (name and email and phone and password):
        return "All fields are required!"

    if not re.match(r"^[0-9]{10}$", phone):
        return "Phone number must be exactly 10 digits!"

    email_pattern = r"^[^ ]+@[^ ]+\.[a-z]{2,3}$"
    if not re.match(email_pattern, email):
        return "Invalid email format!"

    password_pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$"
    if not re.match(password_pattern, password):
        return "Password must contain uppercase, lowercase and a number!"

    # Store name in session
    session["name"] = name

    return redirect(url_for("dashboard"))

# -------------------- DASHBOARD --------------------
@app.route("/dashboard")
def dashboard():
    if "name" not in session:
        return redirect(url_for("home"))

    return render_template("dashboard.html", name=session["name"])

# -------------------- LOGOUT --------------------
@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("home"))

# -------------------- RUN --------------------
if __name__ == "__main__":
    app.run(debug=True)