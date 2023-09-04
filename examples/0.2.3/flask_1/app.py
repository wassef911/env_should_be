import os
from flask import Flask

app = Flask(__name__)
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_PORT = os.environ.get("DB_PORT")
APP_NAME = os.environ.get("APP_NAME")
DEBUG = os.environ.get("DEBUG")


@app.route("/")
def get_app_name():
    return f"You are using {APP_NAME}, made by Mr. {DB_USER}... his database password is {DB_PASSWORD}, please don't hack him."


if __name__ == "__main__":
    app.run(debug=DEBUG)
