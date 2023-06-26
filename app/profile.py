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
from flask_login import current_user, login_required

from . import db
from .models import User

profile = Blueprint('profile', __name__)

@profile.route('/profile')
@login_required
def Index():
    return redirect(url_for("profile.View", id=current_user.id))

@profile.route('/profile/<int:id>')
@login_required
def View(id):
    user = User.query.filter_by(id=id).first()
    if user:
        return render_template('profile/profile.html', user=user)
    else:
        return render_template('error/404.html', message="Profile not found")

@profile.route('/profile/settings/description', methods=['GET', 'POST'])
@login_required
def SettingsDescription():
    if request.method == 'POST':
        new_description = request.form.get('description')
        if len(new_description) > 600+1:
            flash("Максимальная длина: 600 символов")
        else:
            current_user.description = new_description
            db.session.commit()
            return redirect(url_for("profile.View", id=current_user.id))
    return render_template('profile/settings.html')

@profile.route('/profile/settings/email', methods=['GET', 'POST'])
@login_required
def SettingsEmail():
    if request.method == 'POST':
        email = request.form.get('email')

        if email.replace(" ", "") == "":
            flash("Email is empty")
            return redirect(url_for("profile.SettingsEmail"))

        user = User.query.filter_by(email=email).first()
        if user:
            flash("This email already used by someone")
            return redirect(url_for("profile.SettingsEmail"))

        current_user.email = email
        db.session.commit()

        return redirect(url_for("profile.View", id=current_user.id))
    return render_template('profile/email.html')
