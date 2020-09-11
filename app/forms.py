from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Registrar')


class TodosForm(FlaskForm):
    descripcion = StringField('Descripción:', validators=[DataRequired()])
    submit = SubmitField('Crear')


class DeleteTodo(FlaskForm):
    submit = SubmitField('Borrar')
