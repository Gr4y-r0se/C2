from __main__ import app
import sqlite3
import os
from flask import request, make_response
from time import time
from datetime import datetime
from uuid import uuid4
from werkzeug.security import generate_password_hash
from functools import wraps
import random, string


def check_auth(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        cookie = request.cookies.get("auth_cookie")
        resp = make_response()
        connection = sqlite3.connect("db/c2.db")
        cursor = connection.cursor()
        try:
            name, timestamp = cursor.execute(
                """SELECT username,time FROM cookies WHERE cookie = ?""", (cookie,)
            ).fetchall()[0]
            print(name, timestamp)
            if (time() - timestamp) > 600:
                cursor.execute("""DELETE FROM cookies WHERE cookie = ?""", (cookie,))
                raise ValueError
        except Exception as e:
            print(e)
            resp.status = "302"
            resp.headers["Location"] = "/login"
            connection.commit()
            connection.close()
            return resp
        connection.commit()
        connection.close()
        return f(*args, **kwargs)

    return decorator


def setup():
    if os.path.exists("db/c2.db"):
        os.remove("db/c2.db")
    connection = sqlite3.connect("db/c2.db")
    cursor = connection.cursor()
    cursor.execute(
        """CREATE TABLE data (uuid TEXT PRIMARY KEY,
        time_stamp TEXT,
        remote_ip TEXT,
        method TEXT,
        received TEXT,
        owner TEXT NOT NULL)"""
    )
    cursor.execute(
        """CREATE TABLE scripts (uuid TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        owner INT NOT NULL,
        active INT NOT NULL,
        script TEXT NOT NULL)"""
    )
    cursor.execute(
        """CREATE TABLE users (uuid TEXT PRIMARY KEY,
        username TEXT NOT NULL,
        permissions INT NOT NULL,
        identifier TEXT NOT NULL,
        password TEXT NOT NULL)"""
    )
    cursor.execute(
        """CREATE TABLE cookies (uuid TEXT PRIMARY KEY,
        username TEXT,
        cookie TEXT,
        time INT)"""
    )
    cursor.execute(
        """INSERT INTO users (uuid, username, identifier, permissions, password) VALUES (?, ?, ?, ?, ?);""",
        (
            str(uuid4()),
            "admin",
            "".join(
                random.choice(string.ascii_lowercase + string.digits) for _ in range(10)
            ),
            0,
            generate_password_hash(
                "SPIEL-troupe-emir-seeming-pond", method="sha512", salt_length=12
            ),
        ),
    )
    # cursor.execute('''INSERT INTO scripts (uuid, name, owner, active, script) VALUES (?, ?, ?, ?);''',(str(uuid4()),"alert(1)", 1, "alert(1);",))
    # cursor.execute('''INSERT INTO scripts (uuid, name, owner, active, script) VALUES (?, ?, ?, ?, ?);''',(str(uuid4()),"alert cookies", str(uuid4()), 0, "alert(document.cookie);",))
    # move these to register
    connection.commit()
    connection.close()
