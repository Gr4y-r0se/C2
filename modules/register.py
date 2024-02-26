import os
import random
import sqlite3
import string
from datetime import datetime
from time import time
from uuid import uuid4

from __main__ import app
from flask import (
    make_response,
    render_template,
    request,
)
from werkzeug.security import generate_password_hash


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        form_data = request.form
        resp = make_response()
        resp.status = "302"
        connection = sqlite3.connect("db/c2.db")
        cursor = connection.cursor()
        try:
            name = cursor.execute(
                "SELECT username FROM users WHERE username = ?",
                (form_data["username"],),
            ).fetchall()[0]
            resp.headers["Location"] = "/register?error=1"
            return resp
        except:
            pass

        if len(form_data["password"]) < 15:
            resp.headers["Location"] = "/register?error=2"
            return resp

        identifier = "".join(
            random.choice(string.ascii_lowercase + string.digits) for _ in range(10)
        )
        while (
            len(
                cursor.execute(
                    "SELECT username FROM users WHERE identifier = ?", (identifier,)
                ).fetchall()
            )
            > 0
        ):
            identifier = "".join(
                random.choice(string.ascii_lowercase + string.digits) for _ in range(10)
            )
        resp.headers["Location"] = "/login"
        cursor.execute(
            """INSERT INTO users (uuid, username, identifier, permissions, password) VALUES (?, ?, ?, ?, ?);""",
            (
                str(uuid4()),
                form_data["username"],
                "".join(
                    random.choice(string.ascii_lowercase + string.digits)
                    for _ in range(10)
                ),
                1,
                generate_password_hash(
                    form_data["password"], method="sha512", salt_length=12
                ),
            ),
        )

        connection.commit()
        connection.close()
        return resp
    elif request.method == "GET":
        error = request.args.get("error", default=0, type=int)
        return render_template("register.html", name="", error=error)
