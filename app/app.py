from flask import Flask
import os

app = Flask(__name__)


@app.route("/")
def home():
    return "AI DevOps Demo Application - Version 3"


@app.route("/health")
def health():
    return "Application is healthy"


@app.route("/error")
def error():
    raise Exception("Database connection failed")


@app.route("/version")
def version():
    return "Version 1.0"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
