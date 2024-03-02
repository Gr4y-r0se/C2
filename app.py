import os

from flask import Flask

app = Flask(__name__)
app.config["SECRET_KEY"] = "TopS3cret"

from modules import *

if __name__ == "__main__":
    if not os.path.exists("db/c2.db"):
        setup()
    app.run(
        host="0.0.0.0",
        port="443",
        debug=True,
        ssl_context=("certificates/cert.pem", "certificates/key.pem")
    )
