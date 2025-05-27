from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Optional

from app.models import User, IrrigationController
from app import db

users = Blueprint('users', __name__)

class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    first_name = StringField('First Name', validators=[Length(max=64)])
    last_name = StringField('Last Name', validators=[Length(max=64)])
    is_active = BooleanField('Active')
    password = PasswordField('Password', validators=[Optional(), Length(min=8)])
    password2 = PasswordField('Repeat Password', validators=[EqualTo('password')])
    submit = SubmitField('Save')

    def __init__(self, original_username=None, original_email=None, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email

    def validate_username(self, username):
        if self.original_username is None or username.data != self.original_username:
            user = User.query.filter_by(username=username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        if self.original_email is None or email.data != self.original_email:
            user = User.query.filter_by(email=email.data).first()
            if user is not None:
                raise ValidationError('Please use a different email address.')

@users.route('/')
@login_required
def dashboard():
    # Get the irrigation controllers for the current user
    controllers = IrrigationController.query.filter_by(user_id=current_user.id).all()
    
    # Count controllers by moisture level
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

@users.route('/users')
@login_required
def list_users():
    users_list = User.query.all()
    return render_template('users/list.html', title='Users', users=users_list)

@users.route('/users/add', methods=['GET', 'POST'])
@login_required
def add_user():
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
        flash('User created successfully!', 'success')
        return redirect(url_for('users.list_users'))
    return render_template('users/form.html', title='Add User', form=form)

@users.route('/users/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):
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
        flash('User updated successfully!', 'success')
        return redirect(url_for('users.list_users'))
        
    elif request.method == 'GET':
        form.username.data = user.username
        form.email.data = user.email
        form.first_name.data = user.first_name
        form.last_name.data = user.last_name
        form.is_active.data = user.is_active
    
    return render_template('users/form.html', title='Edit User', form=form)

@users.route('/users/delete/<int:id>', methods=['POST'])
@login_required
def delete_user(id):
    user = User.query.get_or_404(id)
    
    if user.id == current_user.id:
        flash('You cannot delete your own account!', 'danger')
    else:
        db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully!', 'success')
    
    return redirect(url_for('users.list_users')) 