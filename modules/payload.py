import sqlite3
from uuid import uuid4
from datetime import datetime
from time import time

from __main__ import app
from flask import render_template, request, session, jsonify

from .support import check_auth


@app.route("/payload/data", methods=["GET"])
@check_auth
def serve_payload_content():
    connection = sqlite3.connect("db/c2.db")
    cursor = connection.cursor()
    id = request.args.get("id", default="", type=str)
    try:
        payload_values = cursor.execute(
            """SELECT name,description,content_type,payload FROM payloads WHERE uuid = ?;""",
            (id,),
        ).fetchall()[0]
    except IndexError:
        payload_values = ['','','','']

    connection.close()

    data = {
        "name": payload_values[0],
        "description": payload_values[1],
        "content_type": payload_values[2],
        "payload": payload_values[3],
    }
    return jsonify(data)

@app.route('/payload/delete/<payload_id>', methods=['DELETE'])
@check_auth
def delete_payload(payload_id):
    try:
        # Connect to the SQLite database
        connection = sqlite3.connect("db/c2.db")
        cursor = connection.cursor()

        # Delete the payload where the id matches
        cursor.execute("DELETE FROM payloads WHERE uuid = ?", (payload_id,))
        
        # Commit the changes
        connection.commit()

        # Check if the row was actually deleted

        return jsonify({"response_text": "Deleted!", "colour": "#FF0000"}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        # Close the connection
        connection.close()
   


@app.route("/payload/publish", methods=["GET"])
@check_auth
def set_payload_active():
    connection = sqlite3.connect("db/c2.db")
    cursor = connection.cursor()
    id = request.args.get("id", default="", type=str)

    payload_value = cursor.execute(
        """SELECT name,description,content_type,payload FROM payloads WHERE uuid = ?;""",
        (id,),
    ).fetchall()[0]

    content = (
        """%s\n\n------$$gr4y-r0se$$------\n\n%s\n\n------$$gr4y-r0se$$------\n\n%s\n\n------$$gr4y-r0se$$------\n\n%s"""
        % (payload_value[0], payload_value[1], payload_value[2], payload_value[3])
    )
    filename = "payloads/%s.txt" % (str(uuid4()))

    with open(filename, "w") as file:
        file.write(content)

    data = {"response_text": "Published!", "colour": "#089305"}
    connection.commit()
    connection.close()
    return jsonify(data)


@app.route("/payload/list", methods=["GET"])
@check_auth
def load_payloads():
    connection = sqlite3.connect("db/c2.db")
    cursor = connection.cursor()
    owner = cursor.execute(
        """SELECT uuid FROM users WHERE username = ?;""", (session["name"],)
    ).fetchall()[0][0]

    payloads = cursor.execute(
            "SELECT uuid,name FROM payloads WHERE owner = ?;",
            (
                owner,
            ),
        ).fetchall()
    data = {}
    for payload in payloads:
        data[payload[0]] = payload[1]

    connection.close()
    return jsonify(data)


@app.route("/payload/save", methods=["POST"])
@check_auth
def save_payload():
    connection = sqlite3.connect("db/c2.db")
    cursor = connection.cursor()
    owner = cursor.execute(
        """SELECT uuid FROM users WHERE username = ?;""", (session["name"],)
    ).fetchall()[0][0]

    form_data = request.form
    try:
        uuid = cursor.execute(
            "SELECT uuid FROM payloads WHERE name = ? AND owner = ?;",
            (
                form_data["name"],
                owner,
            ),
        ).fetchall()[0][0]
        cursor.execute(
            """UPDATE payloads SET payload = ?, description = ?, content_type = ? WHERE uuid = ?;""",
            (
                form_data["the_payload"],
                form_data["description"],
                form_data["content_type"],
                uuid,
            ),
        )
    except:
        cursor.execute(
            """INSERT INTO payloads (uuid, name, description, content_type, payload, owner) VALUES (?, ?, ?, ?, ?, ?);""",
            (
                str(uuid4()),
                form_data["name"],
                form_data["description"],
                form_data["content_type"],
                form_data["the_payload"],
                owner,
            ),
        )
    data = {"response_text": "Saved!", "colour": "#089305"}
    connection.commit()
    connection.close()
    return jsonify(data)


@app.route("/payload", methods=["GET"])
@check_auth
def payload():
    
    host_header = request.headers.get("Host")
    return render_template("payload_edit.html", host=host_header)
