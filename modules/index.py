from __main__ import app
from flask import (
    render_template,
    session,
)


@app.route("/", methods=["GET"])
def index():
    if "name" in session:
        name = session["name"]
    else:
        name = ""
    return render_template("index.html", name=name)
