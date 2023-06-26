"""
    uncat.forum
    Copyright (C) 2023  DonTSmi1e

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from . import db
from .models import User

auth = Blueprint("auth", __name__)

@auth.route("/auth")
def Index():
    if current_user.is_anonymous:
        return render_template("auth/index.html")
    else:
        return redirect(url_for("profile.Index"))

@auth.route("/auth/login", methods=["GET", "POST"])
def Login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password, password):
            flash("Invalid username or password")
            return redirect(url_for('auth.Index'))

        login_user(user, remember=remember)
        return redirect(url_for("index.Index") + ("?showmodal=banModal" if user.ban else ""))
    else:
        return redirect(url_for("auth.Index"))

@auth.route("/auth/signup", methods=["GET", "POST"])
def Signup():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')

        check_1 = email is None or username is None or password is None
        check_2 = email.replace(" ", "") == "" or username.replace(" ", "") == "" or password.replace(" ", "") == ""
        if check_1 or check_2:
            flash("Email, username or password is empty")
            return redirect(url_for('auth.Index'))
        
        if len(username) > 30+1:
            flash('Username max length - 30')
            return redirect(url_for('auth.Index'))
        elif len(password) > 50+1:
            flash('Password max length - 50')
            return redirect(url_for('auth.Index'))

        user_email = User.query.filter_by(email=email).first()
        user_username = User.query.filter_by(username=username).first()

        if user_email:
            flash('This email already registered')
            return redirect(url_for('auth.Index'))
        elif user_username:
            flash('This username already registered')
            return redirect(url_for('auth.Index'))

        new_user = User(email=email,
                        username=username,
                        password=generate_password_hash(password, method='sha256'),
                        description="New account",
                        admin=0,
                        ban=0,
                        points=0)

        db.session.add(new_user)
        db.session.commit()

        user = User.query.filter_by(username=username).first()
        if user.id == 1:
            user.admin = 3
            db.session.commit()

        login_user(User.query.filter_by(username=username).first(), remember=False)
        return redirect(url_for("profile.View", id=user.id) + "?showmodal=welcomeModal")
    else:
        return redirect(url_for("index.Index"))

@auth.route("/auth/logout")
@login_required
def Logout():
    logout_user()
    return redirect(url_for("auth.Index"))
