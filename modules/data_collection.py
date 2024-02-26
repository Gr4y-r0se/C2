import sqlite3
from datetime import datetime
from json import dumps, loads
from time import time
from uuid import uuid4

from __main__ import app
from flask import (
    Flask,
    flash,
    make_response,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from .support import check_auth


@app.route("/collect/<id>", methods=["GET", "POST"])
def collect(id):
    connection = sqlite3.connect("db/c2.db")
    cursor = connection.cursor()
    try:
        owner = cursor.execute(
            """SELECT username FROM users WHERE identifier = ?""", (id,)
        ).fetchall()[0][0]
    except IndexError:
        owner = "admin"
    if request.method == "GET":
        cursor.execute(
            """INSERT INTO data (uuid, time_stamp, remote_ip, method, received, owner) VALUES (?, ?, ?, ?, ? ,?);""",
            (
                str(uuid4()),
                str(datetime.utcfromtimestamp(time()).strftime("%Y-%m-%d %H:%M:%S")),
                str(request.remote_addr),
                "GET",
                "&".join(
                    "%s%s%s"
                    % (k, "=" if request.values[k] != "" else "", request.values[k])
                    for k in request.values
                ),
                owner,
            ),
        )

    elif request.method == "POST":
        placeholder = request.values | loads(request.json) | request.data
        cursor.execute(
            """INSERT INTO data (uuid, time_stamp, remote_ip, method, received, owner) VALUES (?, ?, ?, ?, ?, ?);""",
            (
                str(uuid4()),
                str(datetime.utcfromtimestamp(time()).strftime("%Y-%m-%d %H:%M:%S")),
                str(request.remote_addr),
                "POST",
                "".join("%s: %s" % (k, placeholder) for k in placeholder),
                owner,
            ),
        )

    resp = make_response()
    resp.status = "200"
    connection.commit()
    connection.close()
    resp.headers["P2-C2"] = "C2 Server has received your data :)"
    resp.headers["Access-Control-Allow-Origin"] = "*"
    return resp


@app.route("/clear", methods=["POST"])
# @check_auth
def clear():
    connection = sqlite3.connect("db/c2.db")
    cursor = connection.cursor()
    cursor.execute("""DELETE FROM data WHERE owner = ? """, (session["name"],))
    connection.commit()
    connection.close()
    resp = make_response()
    resp.status = "302"
    resp.headers["Location"] = "/view"
    return resp


@app.route("/view", methods=["GET"])
# @check_auth
def view():
    resp = make_response()
    connection = sqlite3.connect("db/c2.db")
    cursor = connection.cursor()
    data = cursor.execute(
        """SELECT time_stamp, remote_ip, method, received FROM data WHERE owner = ?""",
        (session["name"],),
    ).fetchall()
    connection.commit()
    connection.close()
    return render_template("C2_received.html", content=data, name=session["name"])
