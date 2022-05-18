import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime


# Configure application
app = Flask(__name__)


if __name__ == '__main__':
    app.run()


# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    return flash("Checking")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            flash("Please provide Username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Please provide Password")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash("invalid username and/or password")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

    
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Registering the user when they post
    if request.method == "POST":

        # Get the information from the user
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Check if the username or passwords are not blank
        if not username or not password:
            return apology("Username or Password are missing. Please complete both labels.", 400)

        # Check if password matches confirmation
        elif password != confirmation:
            return apology("Passwords do not match", 400)

        # Require to the user to input numbers and letters
        if password.isnumeric() or len(password) < 6:
            return apology("Please provide a password with a minimum lenght of 6 digits and at least 1 letter or symbol ")

        # Generate hash for password
        pwhash = generate_password_hash(password)

        # Register user into the database only if it is unique
        try:
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, pwhash)
        except:
            return apology("Username already exists. Please select a different one.", 400)

        # Return the user to the login page
        return redirect("/login")

    # If they haven't registered yet it shows the register template
    else:
        return render_template("register.html")


