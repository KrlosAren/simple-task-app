from flask import render_template, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user
from app.forms import LoginForm
from app.models import UserData, UserModel
from . import auth
from app.firestore_service import register_user, get_users, get_user, get_user_id
from werkzeug.security import generate_password_hash, check_password_hash


import uuid


@auth.route('/signup', methods=['GET', 'POST'])
def signup():

    signup_form = LoginForm()
    context = {
        'signup_form': signup_form,
    }

    if signup_form.validate_on_submit():
        username = signup_form.username.data
        password = signup_form.password.data

        user_doc = get_user_id(username=username)

        print(user_doc)

        if user_doc is None:
            uid = uuid.uuid1()
            password_hash = generate_password_hash(password)
            user_data = UserData(uid, username, password_hash)

            register_user(user_data)

            user = UserModel(user_data)
            login_user(user)

            flash(f'Que genial 😁 - Comencemos', 'success')

            return redirect(url_for('main'))

        else:
            flash('Sorry😥. El usuario ya existe.', 'danger')

    return render_template('signup.html', **context)


@auth.route('/login', methods=['GET', 'POST'])
def login():

    login_form = LoginForm()

    context = {
        'login_form': login_form,
    }

    if login_form.validate_on_submit():

        username = login_form.username.data
        password = login_form.password.data

        uid_user = get_user_id(username)
        user_doc = get_user(user_id=uid_user)

        if user_doc.to_dict():
            user_from_db = user_doc.to_dict()['username']
            password_from_db = user_doc.to_dict()['password']

            if check_password_hash(password_from_db, password):
                user_data = UserData(uid_user, username, password)
                user = UserModel(user_data)

                login_user(user)

                flash('Que bueno verte 😁 - Comienza con tus tareas', 'success')
                redirect(url_for('main'))

            else:
                flash('La informacion no coincide 😆', 'danger')

        else:
            flash('El usuario no existe 😅', 'danger')
            return redirect(url_for('auth.login'))

        return redirect(url_for('main'))

    return render_template('login.html', **context)


@auth.route('/logout')
@login_required
def logout():
    logout_user()

    return redirect(url_for('auth.login'))
