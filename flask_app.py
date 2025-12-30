import os

from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash

# Load env files (local dev: .env or prtlnkps.env)
load_dotenv()
load_dotenv("prtlnkps.env")

app = Flask(__name__)
secret_key = os.getenv("SECRET_KEY")
if not secret_key:
    raise RuntimeError("SECRET_KEY is not set; please configure your environment")
app.secret_key = secret_key

@app.route("/")
def index():
    return render_template("main_page.html")

@app.route("/projects")
def projects():
    return render_template("projects.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]
        flash("Your message has been sent successfully!", "success")

        return redirect(url_for("contact"))

    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)
