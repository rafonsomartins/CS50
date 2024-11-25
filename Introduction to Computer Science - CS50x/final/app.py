import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from helpers import error, login_required, clear_partys, clear_bannes
import ast

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///go.db")

@app.route("/")
@login_required
def index():
    bannes = {}
    partys = db.execute("SELECT id, date, house_id FROM partys WHERE id IN (SELECT party_id FROM allowed WHERE group_id IN (SELECT username FROM groups WHERE user_id = ?)) OR house_id IN (SELECT id FROM houses WHERE admin_id = ?) ORDER BY date", session["user_id"], session["user_id"])
    bannes_id = db.execute("SELECT id FROM banned WHERE user_id = ? ORDER BY final_date", session["user_id"])
    if bannes_id:
        for i in range(len(bannes_id)):
            bannes[i] = db.execute("SELECT house_id, final_date FROM banned WHERE id = ?", bannes_id[i]["id"])
            bannes[i][0]["house_id"] = db.execute("SELECT username FROM houses WHERE id = ?", bannes[i][0]["house_id"])[0]["username"]
    for i in range(len(partys)):
        partys[i]["allowed"] = "yes"
    for i in range(len(partys)):
        partys[i]["house_id"] = db.execute("SELECT username FROM houses WHERE id = ?", partys[i]["house_id"])[0]
        for j in range(len(bannes)):
            if bannes[j][0]["house_id"] == partys[i]["house_id"]["username"]:
                if bannes[j][0]["final_date"] >= partys[i]["date"]:
                    partys[i]["allowed"] = "no"
    partys = clear_partys(partys)
    bannes = clear_bannes(bannes)
    return render_template("index.html", partys=partys, bannes=bannes, lenp=len(partys), lenb=len(bannes))

@app.route("/group_management/<sel_gr>/<members>", methods=["GET", "POST"])
@login_required
def group_management(sel_gr, members):
    if request.method == "POST":
        if request.form.get("leave_group"):
            db.execute("DELETE FROM groups WHERE user_id = ? AND username = ?", session["user_id"], sel_gr)
            return render_template("leave_group.html", group=sel_gr)
        elif request.form.get("add_member"):
            return redirect(url_for('add_member', group=sel_gr))
    else:
        str_members = members
        members = ast.literal_eval(members)
        return render_template("group_management.html", username=sel_gr, members=members, sn=str_members)

@app.route("/add_member/<group>", methods=["GET", "POST"])
@login_required
def add_member(group):
    if request.method == "POST":
        added_member = request.form.get("added_member")
        if db.execute("SELECT id FROM users WHERE username = ?", added_member) == 0:
            return error("not existent user", 407)
        if db.execute("SELECT * FROM groups WHERE user_id = ? AND username = ?", added_member, group):
            return error("member already in the group", 408)
        db.execute("INSERT INTO groups (user_id, username) VALUES ((SELECT id FROM users WHERE username = ?), ?)", added_member, group)
        return render_template("member_added.html", member=added_member)
    else:
        return render_template("add_member.html", group=group)

@app.route("/mygroups", methods=["GET", "POST"])
@login_required
def groups():
    if request.method == "POST":
        sel_gr = request.form.get("selected_group")
        members = db.execute("SELECT username FROM users WHERE id IN (SELECT user_id FROM groups WHERE username = ?)", sel_gr)
        return redirect(url_for('group_management', sel_gr=sel_gr, members=members))
    else:
        groups = db.execute("SELECT username FROM groups WHERE user_id = ?", session["user_id"])
        return render_template("groups.html", groups=groups, len=len(groups))

@app.route("/create_group", methods=["GET", "POST"])
@login_required
def create_group():
    if request.method == "POST":
        print("group_username")
        group_username = request.form.get("group_username")
        print("group_username")
        for i in range(4):
            if request.form.get("new_member{}".format(i+1)):
                db.execute("INSERT INTO groups (user_id, username) VALUES ((SELECT id FROM users WHERE username = ?), ?)", request.form.get("new_member{}".format(i+1)), group_username)
        db.execute("INSERT INTO groups (user_id, username) VALUES (?, ?)", session["user_id"], group_username)
        return render_template("group_created.html", group=group_username)
    else:
        return render_template("create_group.html")

@app.route("/myhouses", methods=["GET", "POST"])
def houses():
    if request.method == "POST":
        sel_hou = request.form.get("selected_house")
        house_partys = db.execute("SELECT DISTINCT date, id FROM partys WHERE house_id = (SELECT id FROM houses WHERE username = ?)", sel_hou)
        house_bannes = db.execute("SELECT user_id, final_date, id FROM banned WHERE house_id = (SELECT id FROM houses WHERE username = ?)", sel_hou)
        for i in range(len(house_bannes)):
            house_bannes[i]["user_id"] = db.execute("SELECT username FROM users WHERE id = ?", house_bannes[i]["user_id"])
        return redirect(url_for('house_management', sel_hou=sel_hou, house_partys=house_partys, bannes=house_bannes))
    else:
        houses = db.execute("SELECT username FROM houses WHERE admin_id = ?", session["user_id"])
        return render_template("houses.html", houses=houses, len=len(houses))

@app.route("/house_management/<sel_hou>/<house_partys>/<bannes>", methods=["GET", "POST"])
def house_management(sel_hou, house_partys, bannes):
    if request.method == "POST":
        if request.form.get("delete_house"):
            return redirect(url_for('r_u_sure', house=sel_hou))
        elif request.form.get("add_ban"):
            return redirect(url_for('add_ban', house=sel_hou))
        elif request.form.get("add_party"):
            return redirect(url_for('add_party', house=sel_hou))
        elif request.form.get("delete_ban"):
            db.execute("DELETE FROM banned WHERE id = ?", request.form.get("delete_ban"))
            return render_template("ban_deleted.html", user=db.execute("SELECT username FROM users WHERE id = (SELECT user_id FROM banned WHERE id = ?)", request.form.get("dele_ban")), house=sel_hou)
        elif request.form.get("delete_party"):
            lv = db.execute("DELETE FROM allowed WHERE party_id = ?", request.form.get("delete_party"))
            lv = 1
            if lv:
                db.execute("DELETE FROM partys WHERE id = ?", request.form.get("delete_party"))
                return render_template("party_deleted.html")
            return render_template("ban_deleted.html", user=db.execute("SELECT username FROM users WHERE id = (SELECT user_id FROM banned WHERE id = ?)", request.form.get("dele_ban")), house=sel_hou)
    else:
        str_partys = house_partys
        house_partys = ast.literal_eval(house_partys)
        str_bannes = bannes
        bannes = ast.literal_eval(bannes)
        for party in house_partys:
            party["allowed"] = db.execute("SELECT group_id FROM allowed WHERE party_id = ?", party["id"])
            if party["allowed"]:
                party["allowed"] = party["allowed"][0]["group_id"]
        for ban in bannes:
            ban["user_id"] = ban["user_id"][0]["username"]
        return render_template("house_management.html", username=sel_hou, partys=house_partys, lenp=len(house_partys), sp=str_partys, house_bannes=bannes, lenb=len(bannes), sb=str_bannes)

@app.route("/r_u_sure/<house>", methods=["GET", "POST"])
def r_u_sure(house):
    if request.method == "POST":
        if request.form.get("yes"):
            db.execute("DROP * FROM houses WHERE username = ?", house)
            return render_template("house_deleted.html", house=house)
        else:
            return index()
    else:
        return render_template("r_u_sure.html", house=house)

@app.route("/add_ban/<house>", methods=["GET", "POST"])
def add_ban(house):
    if request.method == "POST":
        if not db.execute("SELECT id FROM users WHERE username = ?", request.form.get("user_username")):
            return error("Not existent username", 411)
        db.execute("INSERT INTO banned (house_id, user_id, final_date) VALUES ((SELECT id FROM houses WHERE username = ?), (SELECT id FROM users WHERE username = ?), ?)", house, request.form.get("user_username"), request.form.get("final_date"))
        return render_template("ban_added.html", username=request.form.get("user_username"), house=house)
    else:
        return render_template("add_ban.html", house=house)

@app.route("/add_party/<house>", methods=["GET", "POST"])
def add_party(house):
    if request.method == "POST":
        db.execute("INSERT INTO partys (house_id, date) VALUES ((SELECT id FROM houses WHERE username = ?), ?)", house, request.form.get("date"))
        for i in range(4):
            mn = request.form.get("group{}".format(i+1))
            if request.form.get("group{}".format(i+1)):
                if not db.execute("SELECT DISTINCT username FROM groups WHERE username = ?", mn):
                    return error("Non existent group username", 412)
                db.execute("INSERT INTO allowed (group_id, party_id) VALUES (?, (SELECT id FROM partys WHERE house_id = (SELECT id FROM houses WHERE username = ?) AND date = ?))", mn, house, request.form.get("date"))
        return render_template("party_added.html", house=house)
    else:
        return render_template("add_party.html", house=house)

@app.route("/create_house", methods=["GET", "POST"])
def create_house():
    if request.method == "POST":
        house_username = request.form.get("house_username")
        db.execute("INSERT INTO houses(username, admin_id) VALUES (?, ?)", house_username, session["user_id"])
        return render_template("house_created.html", house=house_username)
    else:
        return render_template("create_house.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget any user_id
    session.clear()

    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return error("must provide username", 401)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return error("must provide password", 402)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return error("invalid username or password", 403)

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
    session.clear()

    if request.method == "POST":

        if not request.form.get("username"):
            return error("must provide username", 401)

        elif request.form.get("username") in db.execute("SELECT username FROM users"):
            return error("username already exists")

        elif not request.form.get("password"):
            return error("must provide password", 402)

        elif request.form.get("password") != request.form.get("confirmation"):
            return error("confirmation must macth password")

        id = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", request.form.get("username"), generate_password_hash(request.form.get("password")))

        session["user_id"] = id

        return redirect("/")
    else:
        return render_template("register.html")