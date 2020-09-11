from flask import request, make_response, redirect, render_template, session, url_for, flash
from flask_bootstrap import Bootstrap
import unittest
from flask_login import login_required, current_user
from app.forms import TodosForm, DeleteTodo

from app.firestore_service import create_todo, get_user_id, read_todo, delete_todo

from app import create_app

app = create_app()


@app.route('/')
def index():
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
    current_uid = get_user_id(username=current_user.username)

    context = {
        'username': current_user.username,
        'todo_form': todo_form,
        'delete_form': delete_todo,
        'todos': read_todo(user_id=current_uid)
    }

    if todo_form.validate_on_submit():
        create_todo(user_id=current_uid,
                    description=todo_form.descripcion.data)

        flash('La tarea ha sido creada con exito', 'success')

        return redirect(url_for('main'))

    return render_template('main.html', **context)


@app.route('/todo/delete/<todo_id>', methods=['POST'])
def delete(todo_id):
    print(todo_id)
    user_id = get_user_id(username=current_user.username)
    delete_todo(user_id=user_id, todo_id=todo_id)

    flash('La tarea ha sido eliminada', 'success')
    return redirect(url_for('main'))
