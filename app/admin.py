from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user

from .models import User
from .models import Topic
from .models import Message
from . import db

admin = Blueprint('admin', __name__)

@admin.route('/admin')
@login_required
def Index():
    if current_user.admin >= 2:
        return render_template('admin/full.html')
    elif current_user.admin >= 1:
        return render_template('admin/lite.html')
    else:
        return abort(404)

@admin.route('/admin/utils/<int:id>', methods=['POST'])
@login_required
def Utils(id):
    if request.method == "POST" and current_user.ban != 1:
        if id == 1 and current_user.admin >= 1:
            users = User.query.all()
            messages = Message.query.all()
            topics = Topic.query.all()
            for message in messages:
                if not User.query.filter_by(id=message.authorID).first() or not Topic.query.filter_by(id=message.topicID).first():
                    Message.query.filter_by(id=message.id).delete()
            for topic in topics:
                if not User.query.filter_by(id=topic.topicStarter).first():
                    Topic.query.filter_by(id=topic.id).delete()
            for user in users:
                if user.points is None:
                    user.points = 0
            db.session.commit()
        elif id == 2 and current_user.admin >= 2:
            User.query.filter_by(id=int(request.form.get("id"))).delete()
            db.session.commit()
        elif id == 3 and current_user.admin >= 1:
            Topic.query.filter_by(id=int(request.form.get("id"))).delete()
            Message.query.filter_by(topicID=int(request.form.get("id"))).delete()
            db.session.commit()
        elif id == 4 and current_user.admin >= 1:
            user = User.query.filter_by(id=int(request.form.get("id"))).first()
            if user and user.ban == 1 and current_user.admin > user.admin:
                user.ban = 0
            elif user and user.ban == 0 and current_user.admin > user.admin:
                user.ban = 1
            db.session.commit()
        elif id == 5 and current_user.admin >= 2:
            user = User.query.filter_by(id=int(request.form.get("id"))).first()
            if user and current_user.admin > user.admin and int(request.form.get("admin")) in [0, 1, 2]:
                user.admin = int(request.form.get("admin"))
            db.session.commit()
        elif id == 6 and current_user.admin >= 3:
            user = User.query.filter_by(id=int(request.form.get("id"))).first()
            if user and current_user.admin >= 3:
                current_user.admin = 2
                user.admin = 3
            db.session.commit()
        elif id == 7 and current_user.admin >= 2:
            user = User.query.filter_by(id=int(request.form.get("id"))).first()
            user.points += int(request.form.get("points"))
            db.session.commit()

        return redirect(url_for('admin.Index'))
    else:
        return redirect(url_for('index.Index'))
