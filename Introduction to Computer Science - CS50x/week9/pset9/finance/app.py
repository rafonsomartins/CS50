import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    portfolios = db.execute("SELECT symbol, number, user_id FROM stocks WHERE user_id = ?", session["user_id"])
    cash1 = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    grand_total = cash1[0]["cash"]
    for portfolio in portfolios:
        portfolio["user_id"] = lookup(portfolio["symbol"])["price"]
        grand_total += portfolio["user_id"]
    return render_template("index.html", stocks=portfolios, cash=cash1[0]["cash"], Total=grand_total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":

        if not request.form.get("symbol"):
            return apology("must provide symbol")

        stock_buy = lookup(request.form.get("symbol"))

        if not stock_buy:
            return apology("invalide stock")
        else:
            cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
            number = request.form.get("shares")
            total = stock_buy["price"]*float(number)
            if cash < total:
                return apology("insuficient cash")
            else:
                new_cash = cash - (stock_buy["price"]*float(number))
                current_time = datetime.now()
                db.execute("UPDATE users SET cash = ? WHERE id = ?", new_cash, session["user_id"])
                db.execute("INSERT INTO purchases (symbol, price, number, total, user_id, year, month, day, type) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'buy')", stock_buy["symbol"], stock_buy["price"], number, total, session["user_id"], current_time.year, current_time.month, current_time.day)
                number_already = db.execute("SELECT number FROM stocks WHERE user_id = ? AND symbol = ?", session["user_id"], stock_buy["symbol"])
                if db.execute("SELECT symbol FROM stocks WHERE user_id = ? AND symbol = ?", session["user_id"], stock_buy["symbol"]):
                    db.execute("UPDATE stocks SET number = ? WHERE symbol = ? AND user_id = ?", number_already + number, stock_buy["symbol"], session["user_id"])
                    return redirect("/")
                else:
                    db.execute("INSERT INTO stocks (user_id, symbol, number) VALUES (?, ?, ?)", session["user_id"], stock_buy["symbol"], number)
                    return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    transactions = db.execute("SELECT symbol, number, price, total, day, month, year, type FROM purchases WHERE user_id = ? ORDER BY year DESC, month DESC, day DESC LIMIT 30", session["user_id"])
    s = len(transactions)

    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "POST":

        if not request.form.get("symbol"):
            return apology("must provide symbol")

        quoted_stock = lookup(request.form.get("symbol"))

        if not quoted_stock:
            return apology("stock does not exist")

        return render_template("quoted.html", name=(quoted_stock["name"]), symbol=quoted_stock["symbol"], price=usd(quoted_stock["price"]))

    return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    session.clear()

    if request.method == "POST":

        if not request.form.get("username"):
            return apology("must provide username", 400)

        elif request.form.get("username") in db.execute("SELECT username FROM users"):
            return apology("username already exists")

        elif not request.form.get("password"):
            return apology("must provide password", 400)

        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("confirmation must macth password")

        id = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", request.form.get("username"), generate_password_hash(request.form.get("password")))

        session["user_id"] = id

        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "POST":

        if not request.form.get("symbol"):
            return apology("must provide symbol")

        stock_sell = lookup(request.form.get("symbol"))
        if not stock_sell["name"]:
            return apology("invalide stock1")
        if stock_sell["name"] not in db.execute("SELECT DISTINCT symbol FROM stocks WHERE user_id = ?", session["user_id"]):
            return apology("invalid stock2")
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
        number = request.form.get("shares")
        total = db.execute("SELECT number FROM stocks WHERE symbol = ? AND user_id = ?", stock_sell["symbol"], session["user_id"])
        if number > total:
            return apology("insuficient shares")
        else:
            db.execute("INSERT INTO purchases (symbol, price, number, total, user_id, year, month, day, type) VALUES (?, ?, ?, ?, ?, ?, ?, ?, sell)", stock_buy["symbol"], stock_buy["price"], number, number*stock_sell["price"], session["user_id"], current_time.year, current_time.month, current_time.day)
            db.execute("UPDATE users SET cash = ? WHERE id = ?", cash + number*stock_sell["price"], session["user_id"])
            db.execute("UPDATE stocks SET number = ? WHERE symbol = ? AND user_id = ?", total-number, stock_sell["symbol"], session["user_id"])
            return redirect("/")
    else:
        symbols = db.execute("SELECT DISTINCT symbol FROM purchases WHERE user_id = ?", session["user_id"])
        sys = (sy["symbol"] for sy in symbols)
        return render_template("sell.html", stocks=sys)
