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


@app.route("/", methods=["GET"])
def index():
    if "name" in session:
        name = session["name"]
    else:
        name = ""
    return render_template("index.html", name=name)
