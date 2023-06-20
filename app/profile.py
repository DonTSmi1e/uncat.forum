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

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from .models import User
from . import db

profile = Blueprint('profile', __name__)

@profile.route('/profile')
@login_required
def Index():
    return redirect(url_for("profile.View", id=current_user.id))

@profile.route('/profile/<int:id>')
def View(id):
    user = User.query.filter_by(id=id).first()
    if user:
        return render_template('profile/profile.html', user=user)
    else:
        return render_template('error/404.html', message="Profile not found")

@profile.route('/profile/settings', methods=['GET', 'POST'])
@login_required
def Settings():
    if request.method == 'POST':
        new_description = request.form.get('description')
        if len(new_description) > 600+1:
            flash("Максимальная длина: 600 символов")
        else:
            current_user.description = new_description
            db.session.commit()
            return redirect(url_for("profile.View", id=current_user.id))
    return render_template('profile/settings.html')
