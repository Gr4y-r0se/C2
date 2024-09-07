import sqlite3
from uuid import uuid4
from datetime import datetime
from time import time

from __main__ import app
from flask import make_response, render_template, request, session, jsonify

from .support import check_auth


@app.route('/e/<path:subpath>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def serve(subpath):
    resp = make_response()
    connection = sqlite3.connect("db/c2.db")
    cursor = connection.cursor()
    try:
        payload_uuid = cursor.execute(
            """SELECT payload FROM endpoints WHERE identifier = ?""", (subpath,)
        ).fetchall()[0][0]
    except IndexError:
        resp.status = "500"
        return resp
    payload, payload_name, owner = cursor.execute(
        """SELECT script,name FROM scripts WHERE uuid = ?;""", (payload_uuid,)
    ).fetchall()[0]
    cursor.execute(
        """INSERT INTO data (uuid, time_stamp, remote_ip, method, received, owner) VALUES (?, ?, ?, ?, ? ,?);""",
        (
            str(uuid4()),
            str(datetime.fromtimestamp(time()).strftime("%Y-%m-%d %H:%M:%S")),
            str(request.remote_addr),
            "GET",
            "Fetched script titled '%s'" % payload_name,
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


@app.route("/endpoint/data", methods=["GET"])
@check_auth
def serve_script_content():
    connection = sqlite3.connect("db/c2.db")
    cursor = connection.cursor()
    id = request.args.get("id", default="", type=str)

    script_values = cursor.execute(
        """SELECT name,script FROM scripts WHERE uuid = ?;""",
        (id,),
    ).fetchall()[0]

    connection.commit()
    connection.close()

    data = {"script_name": script_values[0], "script": script_values[1]}
    return jsonify(data)


@app.route("/endpoint/save", methods=["POST"])
@check_auth
def save_script():
    connection = sqlite3.connect("db/c2.db")
    cursor = connection.cursor()
    owner = cursor.execute(
        """SELECT uuid FROM users WHERE username = ?;""", (session["name"],)
    ).fetchall()[0][0]

    form_data = request.form
    try:
        uuid = cursor.execute(
            "SELECT uuid FROM scripts WHERE name = ? AND owner = ?;",
            (
                form_data["name"],
                owner,
            ),
        ).fetchall()[0][0]
        cursor.execute(
            """UPDATE scripts SET script = ? WHERE uuid = ?;""",
            (
                form_data["the_script"],
                uuid,
            ),
        )
    except:
        cursor.execute(
            """INSERT INTO scripts (uuid, name, active, script, owner) VALUES (?, ?, ?, ?, ?);""",
            (
                str(uuid4()),
                form_data["name"],
                0,
                form_data["the_script"],
                owner,
            ),
        )
    data = {"response_text": "Saved!", "colour": "#089305"}
    connection.commit()
    connection.close()
    return jsonify(data)


@app.route("/endpoints", methods=["GET"])
@check_auth
def script():
    connection = sqlite3.connect("db/c2.db")
    cursor = connection.cursor()
    owner = cursor.execute(
        """SELECT uuid FROM users WHERE username = ?;""", (session["name"],)
    ).fetchall()[0][0]

    endpoints = cursor.execute(
        """SELECT endpoint,uuid FROM endpoints WHERE owner = ?;""", (owner,)
    ).fetchall()
    endpoints.reverse()
    connection.close()
    host_header = request.headers.get("Host")
    return render_template("endpoints.html", content=endpoints, host=host_header)
