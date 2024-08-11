import sqlite3
from uuid import uuid4
from datetime import datetime
from time import time

from __main__ import app
from flask import (
    make_response,
    render_template,
    request,
    session,
)

from .support import check_auth


@app.route("/<id>/serve.js", methods=["GET"])
def serve(id):
    resp = make_response()
    connection = sqlite3.connect("db/c2.db")
    cursor = connection.cursor()
    try:
        owner = cursor.execute(
            """SELECT uuid FROM users WHERE identifier = ?""", (id,)
        ).fetchall()[0][0]
    except IndexError:
        resp.status = "500"
        return resp
    script, script_name = cursor.execute(
        """SELECT script,name FROM scripts WHERE active = 1 AND owner = ?;""", (owner,)
    ).fetchall()[0]
    cursor.execute(
        """INSERT INTO data (uuid, time_stamp, remote_ip, method, received, owner) VALUES (?, ?, ?, ?, ? ,?);""",
        (
            str(uuid4()),
            str(datetime.fromtimestamp(time()).strftime("%Y-%m-%d %H:%M:%S")),
            str(request.remote_addr),
            "GET",
            "Fetched script titled '%s'" % script_name,
            owner,
        ),
    )  # Log this in 'interactions'
    connection.commit()
    connection.close()
    resp.access_control_allow_origin = "*"
    resp.status = "200"
    resp.mimetype = "text/javascript"
    resp.data = script
    return resp


@app.route("/script", methods=["GET", "POST"])
@check_auth
def save_script():
    connection = sqlite3.connect("db/c2.db")
    cursor = connection.cursor()
    owner = cursor.execute(
        """SELECT uuid FROM users WHERE username = ?;""", (session["name"],)
    ).fetchall()[0][0]
    if request.method == "GET":
        key = request.args.get("name", default="", type=str)

        if key != "":
            cursor.execute(
                """UPDATE scripts SET active = 0 WHERE owner = ?;""", (owner,)
            )
            cursor.execute(
                """UPDATE scripts SET active = ? WHERE name = ? AND owner = ?;""",
                (
                    1,
                    key,
                    owner,
                ),
            )
            connection.commit()
            connection.close()
            resp = make_response()
            resp.status = "200"
            return resp
    elif request.method == "POST":
        form_data = request.form
        try:
            uuid = cursor.execute(
                "SELECT uuid, name, active, script FROM scripts WHERE name = ? AND owner = ?;",
                (
                    form_data["name"],
                    owner,
                ),
            ).fetchall()[0][0]
            cursor.execute(
                """UPDATE scripts SET active = 1, script = ? WHERE uuid = ?;""",
                (
                    form_data["the_script"],
                    uuid,
                ),
            )
        except:
            cursor.execute(
                """UPDATE scripts SET active = 0 WHERE owner = ?;""", (owner,)
            )
            cursor.execute(
                """INSERT INTO scripts (uuid, name, active, script, owner) VALUES (?, ?, ?, ?, ?);""",
                (
                    str(uuid4()),
                    form_data["name"],
                    1,
                    form_data["the_script"],
                    owner,
                ),
            )
    connection.commit()
    scripts = cursor.execute(
        """SELECT name,script FROM scripts WHERE owner = ?;""", (owner,)
    ).fetchall()
    scripts.reverse()
    connection.close()
    return render_template("script_edit.html", content=scripts)
