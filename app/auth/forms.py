"""Authentication forms."""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError

from app.models import User


class LoginForm(FlaskForm):
    """User login form."""
    username = StringField('Nome de usuário', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    remember_me = BooleanField('Lembrar de mim')
    submit = SubmitField('Entrar')


class RegistrationForm(FlaskForm):
    """User registration form."""
    username = StringField(
        'Nome de usuário', 
        validators=[DataRequired(), Length(min=3, max=64)]
    )
    email = StringField(
        'Email', 
        validators=[DataRequired(), Email(), Length(max=120)]
    )
    password = PasswordField(
        'Senha', 
        validators=[DataRequired(), Length(min=8)]
    )
    password2 = PasswordField(
        'Repetir senha', 
        validators=[DataRequired(), EqualTo('password')]
    )
    first_name = StringField('Nome', validators=[Length(max=64)])
    last_name = StringField('Sobrenome', validators=[Length(max=64)])
    submit = SubmitField('Registrar')

    def validate_username(self, username):
        """Validate username uniqueness."""
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Por favor, use um nome de usuário diferente.')

    def validate_email(self, email):
        """Validate email uniqueness."""
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Por favor, use um endereço de email diferente.') 