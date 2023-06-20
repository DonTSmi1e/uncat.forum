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

from flask import Blueprint, render_template
from sqlalchemy import desc
from .models import User
from .models import Topic

index = Blueprint('index', __name__)

@index.route('/')
def Index():
    topics_raw = Topic.query.order_by(Topic.closed, desc(Topic.active)).all()
    topics = []
    for topic in topics_raw:
        topics.append([topic, User.query.filter_by(id=topic.topicStarter).first()])
    return render_template('index.html', users=User.query.order_by(desc(User.admin)).all(), topics=topics)
