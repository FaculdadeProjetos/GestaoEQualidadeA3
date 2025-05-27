"""Authentication routes."""

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.urls import url_parse

from app.models import User
from app.core.extensions import db
from . import auth
from .forms import LoginForm, RegistrationForm


@auth.route('/')
def index():
    """Root route - redirect to login if not authenticated, otherwise to dashboard."""
    if current_user.is_authenticated:
        return redirect(url_for('users.dashboard'))
    return redirect(url_for('auth.login'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """User login route."""
    if current_user.is_authenticated:
        return redirect(url_for('users.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Nome de usuário ou senha inválidos', 'danger')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('users.dashboard')
        
        flash('Login realizado com sucesso!', 'success')
        return redirect(next_page)
    
    return render_template('auth/login.html', title='Entrar', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """User registration route."""
    if current_user.is_authenticated:
        return redirect(url_for('users.dashboard'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data
        )
        db.session.add(user)
        db.session.commit()
        
        flash('Parabéns, você agora é um usuário registrado!', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', title='Registrar', form=form)


@auth.route('/logout')
@login_required
def logout():
    """User logout route."""
    logout_user()
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('auth.login')) 