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

from hashlib import md5
from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(30), unique=True)
	password = db.Column(db.String(50))
	description = db.Column(db.String(200))
	admin = db.Column(db.Integer)
	ban = db.Column(db.Integer)

	def avatar(self, size):
		digest = md5(self.username.encode('utf-8')).hexdigest()
		return f"https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}"

class Topic(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	topicStarter = db.Column(db.Integer)
	title = db.Column(db.String(30))
	closed = db.Column(db.Integer)
	active = db.Column(db.DateTime)

class Message(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	topicID = db.Column(db.Integer)
	authorID = db.Column(db.Integer)
	content = db.Column(db.String(100))
