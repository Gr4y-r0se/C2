import sqlite3
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


@app.route("/<id>/serve.xml", methods=["GET"])
def serve(id):
    resp = make_response()
    connection = sqlite3.connect("db/c2.db")
    cursor = connection.cursor()
    try:
        owner = cursor.execute(
            """SELECT username FROM users WHERE identifier = ?""", (id,)
        ).fetchall()[0][0]
    except IndexError:
        resp.status = "500"
        return resp
    script = cursor.execute(
        """SELECT script FROM scripts WHERE active = 1 AND owner = ?;""", (owner,)
    ).fetchall()[0][0]
    connection.commit()
    connection.close()

    resp.status = "200"
    resp.mimetype = "text/xml"
    resp.data = script
    return resp


@app.route("/script", methods=["GET", "POST"])
# @check_auth
def save_script():
    connection = sqlite3.connect("db/c2.db")
    cursor = connection.cursor()
    if request.method == "GET":
        key = request.args.get("name", default="", type=str)

        if key != "":
            cursor.execute(
                """UPDATE scripts SET active = 0 WHERE owner = ?;""", (session["name"],)
            )
            cursor.execute(
                """UPDATE scripts SET active = ? WHERE name = ? AND owner = ?;""",
                (
                    1,
                    key,
                    session["name"],
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
            uuid, name, active, script = cursor.execute(
                "SELECT uuid, name, active, script FROM scripts WHERE name = ? AND owner = ?;",
                (
                    form_data["name"],
                    session["name"],
                ),
            ).fetchall()[0]
            cursor.execute(
                """UPDATE scripts SET active = 1, script = ? WHERE uuid = ?;""",
                (
                    form_data["the_script"],
                    uuid,
                ),
            )
        except:
            cursor.execute(
                """UPDATE scripts SET active = 0 WHERE owner = ?;""", (session["name"],)
            )
            cursor.execute(
                """INSERT INTO scripts (uuid, name, active, script, owner) VALUES (?, ?, ?, ?, ?);""",
                (
                    str(uuid4()),
                    form_data["name"],
                    1,
                    form_data["the_script"],
                    session["name"],
                ),
            )
    connection.commit()
    scripts = cursor.execute(
        """SELECT name,script FROM scripts WHERE owner = ?;""", (session["name"],)
    ).fetchall()
    scripts.reverse()
    connection.close()
    return render_template("script_edit.html", content=scripts)
