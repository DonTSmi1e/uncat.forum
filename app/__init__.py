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

import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from dotenv import load_dotenv

db = SQLAlchemy()
migrate = Migrate()
loginManager = LoginManager()

def create_app():
    app = Flask(__name__)

    load_dotenv()
    app.config['SECRET_KEY'] = os.environ["SECRET_KEY"]
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    loginManager.login_view = 'auth.Login'

    db.init_app(app)
    migrate.init_app(app, db)
    loginManager.init_app(app)

    from . import models
    from .models import User

    with app.app_context():
        db.create_all()

    @loginManager.user_loader
    def load_user(userID):
        return User.query.get(int(userID))

    @app.errorhandler(404)
    def error_404(e):
        return render_template('error/404.html', message="Page not found"), 404

    @app.errorhandler(Exception)
    def error_500(e):
        return render_template('error/500.html', message=str(e)), 500

    # Route /
    from .index import index as index_blueprint
    app.register_blueprint(index_blueprint)

    # Route /auth
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # Route /profile
    from .profile import profile as profile_blueprint
    app.register_blueprint(profile_blueprint)

    # Route /topic
    from .topic import topic as topic_blueprint
    app.register_blueprint(topic_blueprint)

    # Route /admin
    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)

    return app
