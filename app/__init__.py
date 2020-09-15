from flask import Flask, request, make_response, redirect, render_template, session, url_for, flash
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from .models import UserModel

from .config import Config
from .auth import auth


login_manager = LoginManager()
login_manager.login_view = 'auth.login'

login_manager.login_message = 'Logeate para Organizar tus tareas 😁'
login_manager.login_message_category = 'danger'

@login_manager.user_loader
def load_user(user_id):
    return UserModel.query(user_id)


def create_app():
    app = Flask(__name__)
    bootstrap = Bootstrap(app)

    login_manager.init_app(app)
    app.config.from_object(Config)
    app.register_blueprint(auth)

    return app
