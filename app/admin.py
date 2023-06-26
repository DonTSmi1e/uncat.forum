import datetime

from flask import (Blueprint, abort, flash, redirect, render_template, request,
                   url_for)
from flask_login import current_user, login_required
from sqlalchemy import desc

from . import db
from .models import Log, Message, Topic, User

admin = Blueprint('admin', __name__)

@admin.route('/admin')
@login_required
def Index():
    if current_user.admin >= 2:
        return render_template('admin/index.html')
    return abort(404)

@admin.route("/admin/audit")
@login_required
def AuditLog():
    if current_user.admin >= 1:
        return render_template("admin/auditlog.html", logs=Log.query.order_by(desc(Log.time)).all())
    return redirect(url_for("admin.Index"))

@admin.route("/admin/fixdb")
@login_required
def FixDB():
    if current_user.admin >= 2:
        users = User.query.all()
        for user in users:
            if user.points is None:
                user.points = 0
        db.session.commit()

        db.session.add(Log(category="admin", author=current_user.id, action="Fix database", time=datetime.datetime.now()))
        db.session.commit()

    return redirect(url_for("admin.Index", id=id))

@admin.route("/admin/transferownership", methods=["GET", "POST"])
@login_required
def TransferOwnership():
    if request.method == "POST":
        if current_user.admin >= 3:
            user = User.query.filter_by(id=int(request.form.get("id"))).first()
            if user:
                current_user.admin = 2
                user.admin = 3
            db.session.commit()

            db.session.add(Log(category="admin", author=current_user.id, action=f"Transfer ownership to user {user.id}", time=datetime.datetime.now()))
            db.session.commit()

    return redirect(url_for("index.Index"))

@admin.route("/admin/givepoints", methods=["GET", "POST"])
@login_required
def GivePoints():
    if request.method == "POST":
        if current_user.admin >= 2:
            user = User.query.filter_by(id=int(request.form.get("id"))).first()
            if user:
                user.points += int(request.form.get("points"))
                db.session.commit()

                db.session.add(Log(category="admin", author=current_user.id, action=f"Give {request.form.get('points')} points to user {user.id}", time=datetime.datetime.now()))
                db.session.commit()

    return redirect(url_for("admin.Index"))

@admin.route("/admin/deluser/<int:id>")
@login_required
def DelUser(id):
    user = User.query.filter_by(id=id).first()
    if user and current_user.admin >= 3 and not current_user.id == user.id:
        User.query.filter_by(id=id).delete()
        db.session.commit()

        messages = Message.query.all()
        topics = Topic.query.all()
        for message in messages:
            if not User.query.filter_by(id=message.authorID).first() or not Topic.query.filter_by(id=message.topicID).first():
                Message.query.filter_by(id=message.id).delete()
        for topic in topics:
            if not User.query.filter_by(id=topic.topicStarter).first():
                Topic.query.filter_by(id=topic.id).delete()
        db.session.commit()

        db.session.add(Log(category="admin", author=current_user.id, action=f"Delete user {user.id}", time=datetime.datetime.now()))
        db.session.commit()

    return redirect(url_for("index.Index"))

@admin.route("/admin/promote/<int:id>")
@login_required
def Promote(id):
    if current_user.admin >= 2:
        user = User.query.filter_by(id=id).first()
        if user and not user.admin >= current_user.admin and not user.admin + 1 >= current_user.admin:
            user.admin += 1
            db.session.commit()

            db.session.add(Log(category="admin", author=current_user.id, action=f"Promote user {user.id} to {user.admin}", time=datetime.datetime.now()))
            db.session.commit()

    return redirect(url_for("profile.View", id=id))

@admin.route("/admin/demote/<int:id>")
@login_required
def Demote(id):
    if current_user.admin >= 2:
        user = User.query.filter_by(id=id).first()
        if user and not user.admin >= current_user.admin and not user.admin - 1 < 0:
            user.admin -= 1
            db.session.commit()

            db.session.add(Log(category="admin", author=current_user.id, action=f"Demote user {user.id} to {user.admin}", time=datetime.datetime.now()))
            db.session.commit()

    return redirect(url_for("profile.View", id=id))

@admin.route("/admin/ban/<int:id>")
@login_required
def BanUser(id):
    if current_user.admin >= 1:
        user = User.query.filter_by(id=id).first()
        if user and user.ban == 1 and current_user.admin > user.admin:
            user.ban = 0
        elif user and user.ban == 0 and current_user.admin > user.admin:
            user.ban = 1
        db.session.commit()

        db.session.add(Log(category="admin", author=current_user.id, action=f"Ban/Unban ({user.ban}) user {user.id}", time=datetime.datetime.now()))
        db.session.commit()

    return redirect(url_for("profile.View", id=id))
