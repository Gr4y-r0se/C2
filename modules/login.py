import random
import sqlite3
import string
from time import time
from uuid import uuid4

from __main__ import app
from flask import make_response, render_template, request, session, url_for
from werkzeug.security import check_password_hash

from .support import check_auth


@app.route("/logout", methods=["GET"])
@check_auth
def logout():
    connection = sqlite3.connect("db/c2.db")
    cursor = connection.cursor()
    cursor.execute("""DELETE FROM cookies WHERE username = ?""", (session["name"],))
    session.pop("auth_cookie")
    session.pop("identifier")
    session.pop("name")
    resp = make_response()
    resp.set_cookie("auth_cookie", "", secure=True, httponly=True, samesite="Strict")
    resp.set_cookie("session", "", secure=True, httponly=True, samesite="Strict")
    connection.commit()
    connection.close()
    resp.status = "302"
    resp.headers["Location"] = "/"
    return resp


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        form_data = request.form
        resp = make_response()
        resp.status = "302"
        connection = sqlite3.connect("db/c2.db")
        cursor = connection.cursor()
        try:
            name, h_pass, uuid, identifier = cursor.execute(
                "SELECT username,password,uuid,identifier FROM users WHERE username = ?",
                (form_data["username"],),
            ).fetchall()[0]
        except:
            connection.commit()
            connection.close()
            resp.headers["Location"] = "/login?error=2"
            return resp

        if check_password_hash(h_pass, form_data["password"]):
            resp.headers["Location"] = "/"
            cookie = "".join(
                random.choice(string.ascii_uppercase + string.digits) for _ in range(40)
            )
            cursor.execute(
                "INSERT INTO cookies (uuid,username,cookie,time) VALUES (?, ?, ?, ?);",
                (
                    str(uuid4()),
                    name,
                    cookie,
                    time(),
                ),
            )
            resp.set_cookie(
                "auth_cookie", cookie
            )  # ,secure=True,httponly=True,samesite="Strict")
            session["auth_cookie"] = cookie
            session["name"] = name
            session["identifier"] = identifier
        else:
            resp.headers["Location"] = "/login?error=1"

        connection.commit()
        connection.close()
        return resp
    elif request.method == "GET":
        error = request.args.get("error", default=0, type=int)
        return render_template("login.html", name="", error=error)
