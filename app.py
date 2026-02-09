from flask import Flask, request, render_template, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from models import db, User, location
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
#app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")

mysql_password = os.environ.get("MYSQL_PASSWORD")
users_db = "cascades_users"
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://root:{mysql_password}@localhost/{users_db}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
#db = SQLAlchemy(app)

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

    if current_user:
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
        else:
            return redirect(url_for("signup"))

    if current_user:
        return redirect(url_for("home"))
    
    return render_template("login.html")

@app.route("/setLocation", methods=["POST"])
@login_required
def setLocation():
    if current_user:
        data = request.get_json()
        selected_location = data["location"]
        current_user.loc = selected_location
        db.session.commit()

    return current_user.loc

@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "POST":
        loc = request.form["location"]
        if current_user:
            current_user.loc = loc
            db.session.commit()
        
    return render_template("profile.html", user=current_user)

@app.route("/user/<username>")
def public_profile(username):
    user = User.query.filter_by(username=username).first()
    if user:
        if user == current_user:
            return render_template("profile.html", user=user)    
        return render_template("public_profile.html", user=user)
    else:
        return redirect(url_for("home"))

@app.route("/")
@app.route("/home")
def home():
    location = request.args.get("location")

    if(location):
        if location == "JC":
            users = User.query.filter(or_(User.loc=="JC2", User.loc=="JC3")).all()
        elif location == "Fenwick":
            users = User.query.filter(or_(User.loc=="Fen2", User.loc=="Fen3", User.loc=="Fen4")).all()
        else:
            users = User.query.filter_by(loc=location).all()
    else:
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
