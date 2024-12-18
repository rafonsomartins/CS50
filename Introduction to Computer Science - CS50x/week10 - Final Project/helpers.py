from flask import redirect, render_template, session
from functools import wraps
from datetime import date, datetime

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

def clear_partys(partys):
    new_partys = []
    for i in range(len(partys)):
        partys[i]["date"] = datetime.strptime(partys[i]["date"], '%Y-%m-%d').date()
        if partys[i]["date"] >= date.today():
            new_partys.append(partys[i])
    return new_partys

def clear_bannes(partys):
    new_partys = []
    for i in range(len(partys)):
        partys[i][0]["final_date"] = datetime.strptime(partys[i][0]["final_date"], '%Y-%m-%d').date()
        if partys[i][0]["final_date"] >= date.today():
            new_partys.append(partys[i])
    return new_partys


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