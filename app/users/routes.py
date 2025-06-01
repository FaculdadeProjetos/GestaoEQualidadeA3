"""User management routes."""

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from . import users
from .forms import UserForm
from .services import create_user, update_user, delete_user
from .utils import populate_form_from_user, classify_moisture
from app.models import User, IrrigationController

@users.route('/dashboard')
@login_required
def dashboard():
    controllers = IrrigationController.query.filter_by(user_id=current_user.id).all()
    stats = classify_moisture(controllers)
  
@users.route('/list')
@login_required
def list_users():
    users_list = User.query.all()

@users.route('/add', methods=['GET', 'POST'])
@login_required
def add_user():
    form = UserForm()
    if form.validate_on_submit():
        create_user({
            'username': form.username.data,
            'email': form.email.data,
            'first_name': form.first_name.data,
            'last_name': form.last_name.data,
            'is_active': form.is_active.data,
            'password': form.password.data
        })
        flash('Usuário criado com sucesso!', 'success')
        return redirect(url_for('users.list_users'))

@users.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    user = User.query.get_or_404(id)
    form = UserForm(original_username=user.username, original_email=user.email)

    if form.validate_on_submit():
        update_user(user, {
            'username': form.username.data,
            'email': form.email.data,
            'first_name': form.first_name.data,
            'last_name': form.last_name.data,
            'is_active': form.is_active.data,
            'password': form.password.data
        })
        flash('Usuário atualizado com sucesso!', 'success')

    if request.method == 'GET':
        populate_form_from_user(form, user)


@users.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_user_route(id):
    user = User.query.get_or_404(id)
    if user.id == current_user.id:
        flash('Você não pode deletar sua própria conta!', 'danger')
    else:
        delete_user(user)
        flash('Usuário deletado com sucesso!', 'success')
    return redirect(url_for('users.list_users'))
