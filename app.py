import os
import re

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from flask_mail import Mail, Message
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from itsdangerous import URLSafeTimedSerializer

from helpers import error, login_required


# Configure application
app = Flask(__name__)


# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///goldendot.db")

# Configure e-mail
app.config.from_pyfile("config.cfg")
golden_email = "goldendotgames@gmail.com"
mail = Mail(app)
s = URLSafeTimedSerializer("GoldenSecretKey")

GAMES = [
    {"name": "Dinosaur Escape Jumping", "id": 0},
    {"name": "Roll the Golden Ball", "id": 1},
    {"name": "Golden Search Adventure", "id": 2},
    {"name": "Firefly Discovery", "id": 3}
]

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/games")
def games():
    return render_template("games.html")


@app.route("/news")
def news():
    return render_template("news.html")

@app.route("/search")
def search():
    return render_template("games.html", games=GAMES)

@app.route("/yourgames")
@login_required
def yourgames():
    """List of the favourite games saved by user"""
    
    # Get the user id from the session
    user_id = session["user_id"]

    # Get the current list of favourites
    favourites = db.execute("SELECT * FROM favourites WHERE user_id = ?", user_id)

    # If there are no games in the list, return error
    if len(favourites) < 1:
        return error("You do not have games in favourites yet")

    # Return the page passing the information of the favourites of the user
    return render_template("yourgames.html", favourites=favourites)


@app.route("/add_favourite", methods=["POST"])
@login_required
def add_favourite():
    """Add Favourite user game"""

    # Get the user id from the session
    user_id = session["user_id"]

    # Get the game_id from the item chicked
    game_id = int(request.form.get("id"))
    game_name = GAMES[game_id]["name"]

    # Check if the game is already in the list
    favourites = db.execute("SELECT * FROM favourites WHERE user_id = ? AND game_id = ?", user_id, game_id)
    if len(favourites) != 0:
        return error("Your game is already one of your favourites")

    # Add the game to the favourite games
    db.execute("INSERT INTO favourites (user_id, game_id, game_name) VALUES (?, ?, ?)", 
               user_id, game_id, game_name)

    # Redirect to Your Games site
    return redirect("/yourgames")


@app.route("/remove_favourite", methods=["POST"])
@login_required
def remove_favourite():
    """Remove Favourite user's game"""

    # Get the user id from the session
    user_id = session["user_id"]

    # Get the game_id from the item chicked
    game_id = request.form.get("id")

    # Check that the game is in the list
    favourites = db.execute("SELECT * FROM favourites WHERE user_id = ? AND game_id = ?", user_id, game_id)
    if len(favourites) == 0:
        return error("Your game is not in the list of your favourites")

    # Remove the game to the favourite games
    db.execute("DELETE FROM favourites WHERE user_id = ? AND game_id = ?", 
               user_id, game_id)

    # Redirect to Your Games site
    return redirect("/yourgames")


@app.route("/contactus", methods=["GET", "POST"])
def contactus():
    """Form used by users to leave messages"""

    if request.method == "POST":

        # Get the information from the form
        name = request.form.get("name")
        email = request.form.get("email")
        user_message = request.form.get("message")

        # Send e-mail from user
        message = Message("Golden DOT Games Website - Message from user {}".format(name),
                          recipients=[golden_email])
        message.body = "A user has sent a message as follows: {}".format(user_message)
        mail.send(message)

        # Confirm the user that the message has been received
        try:
            message_confirmation = Message("Golden DOT Games Website - Thanks for your message", 
                                           recipients=[email])
            message_confirmation.body = "You have sent a message to Golden DOT Games Website. Thanks!"
            mail.send(message_confirmation)
        except:
            error("Your email failed but your message has been sent")
        
        return redirect("/")

    # Render the template to confirm the information
    else:
        return render_template("contactus.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return error("Please provide Username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return error("Please provide Password")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return error("Invalid username and/or password")

        # Ensure the user has confirmed the email
        user_e_confirm = rows[0]["e_confirm"]
        if int(user_e_confirm) == 0:
            return error("You must validate your email with the link we have sent")

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
        email = request.form.get("email")

        # Check if the username, email or passwords are not blank
        if not username or not password or not email:
            return error("Username or Password are missing. Please complete both labels.")

        # Check if password matches confirmation
        elif password != confirmation:
            return error("Passwords do not match")

        # Require to the user to input numbers and letters
        if password.isnumeric() or len(password) < 6:
            return error("Please provide a password with a minimum lenght of 6 digits and at least 1 letter or symbol ")

        # Generate hash for password
        pwhash = generate_password_hash(password)

        # Register user into the database only if it is unique
        try:
            db.execute("INSERT INTO users (username, hash, email) VALUES (?, ?, ?)", username, pwhash, email)
        except:
            return error("Username already exists. Please select a different one.")

        # Make the URL to confirm email is functional
        token = s.dumps(email)
        link = url_for("confirm_email", token=token, external=True)

        # Send e-mail
        message = Message("Welcome to Golden DOT Games! Your e-mail must be confirmed", recipients=[email])
        message.body = "Your link is {}".format(link)
        mail.send(message)

        # Return the user to the login page
        return redirect("/login")

    # If they haven't registered yet it shows the register template
    else:
        return render_template("register.html")

@app.route("/confirm_email/<token>")
def confirm_email(token):
    """Confirm the e-mail with the token"""

    # Try to validate the token provided, and if not, get an error message
    try:
        email = s.loads(token, max_age=300)
    except:
        return error("Your token is incorrect or expired")

    # Modify the information in the database to set the user with a confirmed email
    db.execute("UPDATE users SET e_confirm = 1 WHERE email= ? ", email)
    return redirect("/login")