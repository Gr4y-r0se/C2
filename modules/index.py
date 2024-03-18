from __main__ import app
from flask import (
    render_template,
    session,
    redirect,
    url_for
)


@app.route("/", methods=["GET"])
def index():
    if "name" in session:
        name = session["name"]
    else:
        name = ""
        return redirect(url_for("login"))
    return render_template("index.html", name=name)
