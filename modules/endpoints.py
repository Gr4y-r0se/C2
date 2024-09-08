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
        payload_uuid, owner = cursor.execute(
            """SELECT payload,owner FROM endpoints WHERE endpoint = ?""", (subpath,)
        ).fetchall()[0]
    except IndexError:
        resp.status = "500"
        return resp

    try:
        payload, payload_name, content_type = cursor.execute(
            """SELECT payload,name,content_type FROM payloads WHERE uuid = ?;""", (payload_uuid,)
        ).fetchall()[0]
    except:
        payload, payload_name, content_type = ['blank','blank','blank']

    cursor.execute(
        """INSERT INTO data (uuid, time_stamp, remote_ip, method, received, owner) VALUES (?, ?, ?, ?, ? ,?);""",
        (
            str(uuid4()),
            str(datetime.fromtimestamp(time()).strftime("%Y-%m-%d %H:%M:%S")),
            str(request.remote_addr),
            request.method,
            "Fetched script '%s' from endpoint '%s'" %(payload_name,subpath),
            owner,
        ),
    )  # Log this in 'interactions'
    connection.commit()
    connection.close()
    resp.access_control_allow_origin = "*"
    resp.status = "200"
    resp.mimetype = content_type
    resp.data = payload
    resp.headers['X-Payload-Name'] = payload_name
    return resp


@app.route("/endpoints/list", methods=["GET"])
@check_auth
def load_endpoints():
    connection = sqlite3.connect("db/c2.db")
    cursor = connection.cursor()
    owner = cursor.execute(
        """SELECT uuid FROM users WHERE username = ?;""", (session["name"],)
    ).fetchall()[0][0]

    endpoints = cursor.execute(
            "SELECT uuid,name,endpoint,description,payload,method FROM endpoints WHERE owner = ?;",
            (
                owner,
            ),
        ).fetchall()
    data = []
    for endpoint in endpoints:
        payload_name = cursor.execute(
            "SELECT name FROM payloads WHERE owner = ? AND uuid = ?;",
            (
                owner,
                endpoint[4],
            ),
        ).fetchall()
        data.append({
            "uuid":endpoint[0],
            "name":endpoint[1],
            "endpoint":endpoint[2],
            "description":endpoint[3],
            "payload":payload_name,
            "method":endpoint[5]
        })

    connection.close()
    return jsonify(data)

@app.route("/endpoints/data", methods=["GET"])
@check_auth
def load_endpoint_data():
    connection = sqlite3.connect("db/c2.db")
    cursor = connection.cursor()
    owner = cursor.execute(
        """SELECT uuid FROM users WHERE username = ?;""", (session["name"],)
    ).fetchall()[0][0]
    id = request.args.get("id", default="", type=str)
    try:
        endpoint = cursor.execute(
            "SELECT uuid,name,endpoint,description,payload,method FROM endpoints WHERE owner = ? AND uuid = ?;",
            (
                owner,
                id,
            ),
        ).fetchall()[0]
        
    except IndexError:
        endpoint = ['','','','','','']

    connection.close()

    data = {
            "uuid":endpoint[0],
            "name":endpoint[1],
            "endpoint":endpoint[2],
            "description":endpoint[3],
            "payload":endpoint[4],
            "method":endpoint[5]
        }
    
    return jsonify(data),200

@app.route("/endpoint/save", methods=["POST"])
@check_auth
def save_script():
    connection = sqlite3.connect("db/c2.db")
    cursor = connection.cursor()
    owner = cursor.execute(
        """SELECT uuid FROM users WHERE username = ?;""", (session["name"],)
    ).fetchall()[0][0]

    form_data = request.form
    uuid = form_data['uuid']
    if uuid != '':
        cursor.execute(
            """UPDATE endpoints SET name = ?, endpoint = ?, description = ?, payload = ?, method = ? WHERE uuid = ?;""",
            (
                form_data["name"],
                form_data["endpoint"],
                form_data["description"],
                form_data["payload"],
                form_data["method"],
                uuid,
            ),
        )
    else:
        cursor.execute(
            """INSERT INTO endpoints (uuid, name, endpoint, description, payload, method, owner) VALUES (?, ?, ?, ?, ?, ?, ?);""",
            (
                str(uuid4()),
                form_data["name"],
                form_data["endpoint"],
                form_data["description"],
                form_data["payload"],
                form_data["method"],
                owner,
            ),
        )
    data = {"response_text": "Saved!", "colour": "#089305"}
    connection.commit()
    connection.close()
    return jsonify(data)


@app.route('/endpoint/delete/<endpoint_id>', methods=['DELETE'])
@check_auth
def delete_endpoint(endpoint_id):
    connection = sqlite3.connect("db/c2.db")
    cursor = connection.cursor()
    owner = cursor.execute(
        """SELECT uuid FROM users WHERE username = ?;""", (session["name"],)
    ).fetchall()[0][0]
    try:


        # Delete the payload where the id matches
        cursor.execute("DELETE FROM endpoints WHERE uuid = ? AND owner = ?", (endpoint_id,owner,))
        print(endpoint_id,owner)
        # Commit the changes
        connection.commit()
        # Close the connection
        connection.close()

        # Check if the row was actually deleted

        return jsonify({"response_text": "Deleted!", "colour": "#FF0000"}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
        

@app.route("/endpoints", methods=["GET"])
@check_auth
def endpoints():
    host_header = request.headers.get("Host")
    return render_template("endpoints.html", host=host_header)
