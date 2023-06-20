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

import datetime
from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_login import current_user, login_required
from .models import User
from .models import Topic
from .models import Message
from . import db

topic = Blueprint('topic', __name__)

@topic.route('/topic/<int:id>', methods=['GET', 'POST'])
def View(id):
    topic = Topic.query.filter_by(id=id).first()
    if topic:
        if request.method == "POST":
            if not topic.closed:
                message = request.form.get("message")

                startMessage = Message(topicID=topic.id, authorID=current_user.id, content=message)
                db.session.add(startMessage)
                db.session.commit()

            return redirect(url_for("topic.View", id=topic.id))
        else:
            messages_raw = Message.query.filter_by(topicID=topic.id).all()
            messages = []
            for message in messages_raw:
                messages.append([message, User.query.filter_by(id=message.authorID).first()])

            topicStarter = User.query.filter_by(id=topic.topicStarter).first()

            return render_template("topic/view.html", topic=topic, topicStarter=topicStarter, messages=messages)
    else:
        return render_template('error/404.html', message="This topic does not exists")

@topic.route('/topic/create', methods=['GET', 'POST'])
@login_required
def Create():
    if request.method == 'POST':
        if current_user.ban != 1:
            title = request.form.get('title')
            message = request.form.get('message')

            topic = Topic.query.filter_by(title=title).first()

            if title.replace(" ", "") == "" or message.replace(" ", "") == "":
                flash('Title or message cannot be empty')
                return redirect(url_for('topic.Create', title=title, content=message))

            if topic:
                flash('Topic with this title already exists')
                return redirect(url_for('topic.Create', title=title, content=message))

            if len(title) > 100+1:
                flash('Title max length: 100')
                return redirect(url_for('topic.Create', title=title, content=message))
            elif len(message) > 1500+1:
                flash('Message max length: 1500')
                return redirect(url_for('topic.Create', title=title, content=message))

            topic = Topic(topicStarter=current_user.id, title=title, active=datetime.datetime.now(), closed=0)
            db.session.add(topic)
            db.session.commit()

            topic = Topic.query.filter_by(title=title).first()
            startMessage = Message(topicID=topic.id, authorID=topic.topicStarter, content=message)
            db.session.add(startMessage)
            db.session.commit()

            return redirect(url_for('topic.View', id=topic.id))
        else:
            flash('You have been banned')
            return redirect(url_for('topic.Create'))
    else:
        return render_template('topic/create.html', title=request.args.get('title'), content=request.args.get('content'))

@topic.route('/topic/utils/delmessage/<int:id>')
@login_required
def DelMessage(id):
    message = Message.query.filter_by(id=id).first()
    if message:
        topicID = message.topicID
        if current_user.admin > 0 or current_user.id == message.authorID:
            Message.query.filter_by(id=id).delete()
            db.session.commit()
        return redirect(url_for("topic.View", id=topicID))
    else:
        return redirect(url_for("index.Index"))

@topic.route('/topic/utils/changestatus/<int:id>')
@login_required
def Status(id):
    topic = Topic.query.filter_by(id=id).first()
    if topic:
        if current_user.admin > 0 or current_user.id == topic.topicStarter:
            topic.closed = 0 if topic.closed else 1
            db.session.commit()
        return redirect(url_for("topic.View", id=id))
    else:
        return redirect(url_for("index.Index"))
