from __main__ import app
import sqlite3
from os import listdir, path, remove
from flask import request, make_response, session
from time import time
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

            if (time() - timestamp) > 7200:
                cursor.execute("""DELETE FROM cookies WHERE cookie = ?""", (cookie,))
                raise ValueError
        except Exception as e:
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
    # Remove the existing database if it exists
    if path.exists("db/c2.db"):
        remove("db/c2.db")

    # Connect to the new database
    connection = sqlite3.connect("db/c2.db")
    cursor = connection.cursor()

    # Create the 'data' table
    cursor.execute(
        """CREATE TABLE data (
            uuid TEXT PRIMARY KEY,
            time_stamp TEXT,
            remote_ip TEXT,
            method TEXT,
            received TEXT,
            owner TEXT NOT NULL
        )"""
    )

    # Create the 'payloads' table
    cursor.execute(
        """CREATE TABLE payloads (
            uuid TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            owner INT NOT NULL,
            description TEXT,
            payload TEXT NOT NULL,
            content_type TEXT NOT NULL
        )"""
    )

    # Create the 'users' table
    cursor.execute(
        """CREATE TABLE users (
            uuid TEXT PRIMARY KEY,
            username TEXT NOT NULL,
            permissions INT NOT NULL,
            identifier TEXT NOT NULL,
            password TEXT NOT NULL
        )"""
    )

    # Create the 'cookies' table
    cursor.execute(
        """CREATE TABLE cookies (
            uuid TEXT PRIMARY KEY,
            username TEXT,
            cookie TEXT,
            time INT
        )"""
    )

    # Create the new 'endpoints' table
    cursor.execute(
        """CREATE TABLE endpoints (
            uuid TEXT PRIMARY KEY,
            id TEXT NOT NULL,
            endpoint TEXT NOT NULL,
            description TEXT,
            method TEXT NOT NULL,
            owner TEXT NOT NULL
        )"""
    )

    # Admin setup
    admin_id = str(uuid4())
    admin_password = "".join(
        random.choice(string.ascii_lowercase + string.digits) for _ in range(15)
    )

    print("\n\n\tNew deployment detected. Admin password is: %s\n\n" % (admin_password))

    cursor.execute(
        """INSERT INTO users (uuid, username, identifier, permissions, password) VALUES (?, ?, ?, ?, ?);""",
        (
            admin_id,
            "admin",
            "".join(
                random.choice(string.ascii_lowercase + string.digits) for _ in range(10)
            ),
            0,
            generate_password_hash(admin_password, method="sha512", salt_length=12),
        ),
    )

    # Load JavaScript files into the 'scripts' table
    for filename in listdir("payloads/"):
        if filename.endswith(".txt"):
            filepath = path.join("./payloads/", filename)
            with open(filepath, "r") as file:
                content = file.read()
                title, description, content_type, payload = content.split(
                    "\n\n------$$gr4y-r0se$$------\n\n"
                )

                cursor.execute(
                    """INSERT INTO payloads (uuid, name, description, owner, content_type, payload) VALUES (?, ?, ?, ?, ?, ?);""",
                    (
                        str(uuid4()),
                        title,
                        description,
                        admin_id,
                        content_type,
                        payload,
                    ),
                )

    # Commit and close the connection
    connection.commit()
    connection.close()
