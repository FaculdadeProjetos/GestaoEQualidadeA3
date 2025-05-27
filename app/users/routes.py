"""User management routes."""

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Optional

from app.models import User, IrrigationController
from app.core.extensions import db
from . import users


class UserForm(FlaskForm):
    """Form for user creation and editing."""
    username = StringField('Nome de usuário', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    first_name = StringField('Nome', validators=[Length(max=64)])
    last_name = StringField('Sobrenome', validators=[Length(max=64)])
    is_active = BooleanField('Ativo')
    password = PasswordField('Senha', validators=[Optional(), Length(min=8)])
    password2 = PasswordField('Repetir senha', validators=[EqualTo('password')])
    submit = SubmitField('Salvar')

    def __init__(self, original_username=None, original_email=None, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email

    def validate_username(self, username):
        """Validate username uniqueness."""
        if self.original_username is None or username.data != self.original_username:
            user = User.query.filter_by(username=username.data).first()
            if user is not None:
                raise ValidationError('Por favor, use um nome de usuário diferente.')

    def validate_email(self, email):
        """Validate email uniqueness."""
        if self.original_email is None or email.data != self.original_email:
            user = User.query.filter_by(email=email.data).first()
            if user is not None:
                raise ValidationError('Por favor, use um endereço de email diferente.')


@users.route('/dashboard')
@login_required
def dashboard():
    """User dashboard with irrigation controllers overview."""
    controllers = IrrigationController.query.filter_by(user_id=current_user.id).all()
    
    low_moisture = 0
    medium_moisture = 0
    good_moisture = 0
    
    for controller in controllers:
        if controller.moisture_level < 30:
            low_moisture += 1
        elif controller.moisture_level < 60:
            medium_moisture += 1
        else:
            good_moisture += 1
    
    return render_template('users/dashboard.html', 
                           title='Dashboard',
                           controllers=controllers,
                           controller_count=len(controllers),
                           low_moisture=low_moisture,
                           medium_moisture=medium_moisture,
                           good_moisture=good_moisture)


@users.route('/list')
@login_required
def list_users():
    """List all users."""
    users_list = User.query.all()
    return render_template('users/list.html', title='Usuários', users=users_list)


@users.route('/add', methods=['GET', 'POST'])
@login_required
def add_user():
    """Add new user."""
    form = UserForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data
        )
        user.is_active = form.is_active.data
        db.session.add(user)
        db.session.commit()
        flash('Usuário criado com sucesso!', 'success')
        return redirect(url_for('users.list_users'))
    return render_template('users/form.html', title='Adicionar Usuário', form=form)


@users.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    """Edit existing user."""
    user = User.query.get_or_404(id)
    form = UserForm(original_username=user.username, original_email=user.email)
    
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.is_active = form.is_active.data
        
        if form.password.data:
            user.set_password(form.password.data)
            
        db.session.commit()
        flash('Usuário atualizado com sucesso!', 'success')
        return redirect(url_for('users.list_users'))
        
    elif request.method == 'GET':
        form.username.data = user.username
        form.email.data = user.email
        form.first_name.data = user.first_name
        form.last_name.data = user.last_name
        form.is_active.data = user.is_active
    
    return render_template('users/form.html', title='Editar Usuário', form=form)


@users.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_user(id):
    """Delete user."""
    user = User.query.get_or_404(id)
    
    if user.id == current_user.id:
        flash('Você não pode deletar sua própria conta!', 'danger')
    else:
        db.session.delete(user)
        db.session.commit()
        flash('Usuário deletado com sucesso!', 'success')
    
    return redirect(url_for('users.list_users')) 