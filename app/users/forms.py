from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional

class UserForm(FlaskForm):
    username = StringField('Nome de usuário', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    first_name = StringField('Nome', validators=[Length(max=64)])
    last_name = StringField('Sobrenome', validators=[Length(max=64)])
    is_active = BooleanField('Ativo')
    password = PasswordField('Senha', validators=[Optional(), Length(min=8)])
    password2 = PasswordField('Repetir senha', validators=[EqualTo('password')])
    submit = SubmitField('Salvar')