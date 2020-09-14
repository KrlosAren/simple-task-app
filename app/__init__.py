from flask import Flask, request, make_response, redirect, render_template, session, url_for, flash
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from .models import UserModel
from flask_wtf import CsrfProtect
from flask_cors import CORS

from .config import Config
from .auth import auth


login_manager = LoginManager()
login_manager.login_view = 'auth.login'
csrf = CsrfProtect()


@login_manager.user_loader
def load_user(user_id):
    return UserModel.query(user_id)


def create_app():
    app = Flask(__name__)
    bootstrap = Bootstrap(app)
    app.config.update(
        DEBUG=False,
        ENV='development'
    )

    csrf.init_app(app)
    login_manager.init_app(app)
    CORS(app)
    app.config.from_object(Config)
    app.register_blueprint(auth)

    return app
