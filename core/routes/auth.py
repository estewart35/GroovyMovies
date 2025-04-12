from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from core.models import Users
from core import db

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
   if request.method == "POST":
       email = request.form.get("email")
       password = request.form.get("password")
       user = Users.query.filter_by(email=email).first()
       if user and user.check_password(password):
           login_user(user)
           flash("Logged in successfully!", "success")
           return redirect(url_for("web.profile"))
       else:
           flash("Invalid email or password", "danger")
   return render_template("auth/login.html", user=current_user)


@auth.route("/register", methods=["GET", "POST"])
def register():
   if request.method == "POST":
       email = request.form.get("email")
       password = request.form.get("password")
       user = Users.query.filter_by(email=email).first()
       if user:
           flash("Email already exists.", "danger")
       else:
           new_user = Users(email=email)
           new_user.set_password(password)
           db.session.add(new_user)
           db.session.commit()
           flash("Account created!", "success")
           return redirect(url_for("auth.login"))
   return render_template("auth/register.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
   logout_user()
   flash("Logged out successfully!", "info")
   return redirect(url_for("auth.login"))