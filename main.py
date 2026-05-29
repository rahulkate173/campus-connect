from flask import render_template, redirect, url_for, session
from app import create_app

app = create_app()


@app.route("/")
def index():
    """Landing page."""
    user = session.get("user")
    return render_template("index.html", user=user)


@app.route("/home")
def home():
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)
