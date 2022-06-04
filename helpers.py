import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps
from datetime import datetime
from newsapi import NewsApiClient

def error(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("error.html", top=code, bottom=escape(message)), code

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def get_news(date):

    try:
        api_key = "36bc40bccb9b4db3bef3fa509115e019"
        url = f"https://newsapi.org/v2/everything?q=videogames&language=en&from={date}&apiKey={api_key}"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None

    try:
        data = response.json()
        return data

    except (KeyError, TypeError, ValueError):
        return None