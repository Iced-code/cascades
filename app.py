from flask import Flask, request, render_template, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import db, User, location
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))




@app.route('/signup', methods=["GET","POST"])
def signup():
    if request.method == "POST":
        name = request.form["username"]
        username = request.form["username"]
        email = request.form["email"]

        user = User(name=name, username=username, email=email)
        db.session.add(user)
        db.session.commit()

        login_user(user)
        return redirect(url_for("home"))

    return render_template("signup.html")

@app.route('/login', methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        user = User.query.filter_by(username=username).first()

        if user:
            login_user(user)
            return redirect(url_for("home"))

    return render_template("login.html")

@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user=current_user)

@app.route("/user/<username>")
def public_profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    if user == current_user:
        return render_template("profile.html", user=user)    
    return render_template("public_profile.html", user=user)

@app.route("/")
@app.route("/home")
def home():
    users = User.query.all()
    return render_template("home.html", users=users)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
