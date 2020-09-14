from flask import request, make_response, redirect, render_template, session, url_for, flash, request
from flask_bootstrap import Bootstrap
import unittest
from flask_login import login_required, current_user
from app.forms import TodosForm, DeleteTodo, UpdateTodo

from app.firestore_service import create_todo, get_user_id, read_todo, delete_todo, update_todo

from app import create_app

app = create_app()


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)


@app.errorhandler(500)
def server_not_found(error):
    return render_template('505.html', error=error)


@app.route('/')
def index():
    print(request.remote_addr)
    return redirect(url_for('home'))


@app.route('/home')
def home():

    context = {
    }
    return render_template('index.html', **context)


@app.route('/main', methods=['GET', 'POST'])
@login_required
def main():

    todo_form = TodosForm()
    delete_todo = DeleteTodo()
    update_todo = UpdateTodo()
    current_uid = get_user_id(username=current_user.username)

    context = {
        'username': current_user.username,
        'todo_form': todo_form,
        'delete_form': delete_todo,
        'todos': read_todo(user_id=current_uid),
        'update_form': update_todo,
    }

    if todo_form.validate_on_submit():
        create_todo(user_id=current_user.id,
                    description=todo_form.descripcion.data)

        flash('La tarea ha sido creada con exito 🥳', 'success')

        return redirect(url_for('main'))

    return render_template('main.html', **context)


@app.route('/todo/delete/<todo_id>', methods=['POST'])
def delete(todo_id):
    user_id = get_user_id(username=current_user.username)
    delete_todo(user_id=user_id, todo_id=todo_id)

    flash('La tarea ha sido eliminada 😁', 'success')
    return redirect(url_for('main'))


@app.route('/todo/update/<todo_id>/<int:done>', methods=['POST'])
def update(todo_id, done):
    user_id = get_user_id(username=current_user.username)
    update_todo(user_id=user_id, todo_id=todo_id, done=done)

    flash('La tarea ha sido actualizada 😎', 'success')
    return redirect(url_for('main'))
