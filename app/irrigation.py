from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, BooleanField, SubmitField, DateTimeField
from wtforms.validators import DataRequired, Length, NumberRange, Optional

from app.models import IrrigationController
from app import db
from datetime import datetime

irrigation = Blueprint('irrigation', __name__)

class IrrigationControllerForm(FlaskForm):
    name = StringField('Controller Name', validators=[DataRequired(), Length(min=3, max=100)])
    moisture_level = FloatField('Moisture Level (%)', validators=[DataRequired(), NumberRange(min=0, max=100)])
    is_active = BooleanField('Active')
    submit = SubmitField('Save')

@irrigation.route('/irrigation')
@login_required
def list_controllers():
    controllers = IrrigationController.query.filter_by(user_id=current_user.id).all()
    return render_template('irrigation/list.html', title='Irrigation Controllers', controllers=controllers)

@irrigation.route('/irrigation/add', methods=['GET', 'POST'])
@login_required
def add_controller():
    form = IrrigationControllerForm()
    if form.validate_on_submit():
        controller = IrrigationController(
            name=form.name.data,
            moisture_level=form.moisture_level.data,
            is_active=form.is_active.data,
            user_id=current_user.id
        )
        db.session.add(controller)
        db.session.commit()
        flash('Irrigation controller created successfully!', 'success')
        return redirect(url_for('irrigation.list_controllers'))
    return render_template('irrigation/form.html', title='Add Irrigation Controller', form=form)

@irrigation.route('/irrigation/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_controller(id):
    controller = IrrigationController.query.get_or_404(id)
    
    # Check if the controller belongs to the current user
    if controller.user_id != current_user.id:
        flash('You do not have permission to edit this controller', 'danger')
        return redirect(url_for('irrigation.list_controllers'))
    
    form = IrrigationControllerForm()
    
    if form.validate_on_submit():
        controller.name = form.name.data
        controller.moisture_level = form.moisture_level.data
        controller.is_active = form.is_active.data
        
        db.session.commit()
        flash('Irrigation controller updated successfully!', 'success')
        return redirect(url_for('irrigation.list_controllers'))
        
    elif request.method == 'GET':
        form.name.data = controller.name
        form.moisture_level.data = controller.moisture_level
        form.is_active.data = controller.is_active
    
    return render_template('irrigation/form.html', title='Edit Irrigation Controller', form=form)

@irrigation.route('/irrigation/delete/<int:id>', methods=['POST'])
@login_required
def delete_controller(id):
    controller = IrrigationController.query.get_or_404(id)
    
    # Check if the controller belongs to the current user
    if controller.user_id != current_user.id:
        flash('You do not have permission to delete this controller', 'danger')
    else:
        db.session.delete(controller)
        db.session.commit()
        flash('Irrigation controller deleted successfully!', 'success')
    
    return redirect(url_for('irrigation.list_controllers'))

@irrigation.route('/irrigation/irrigate/<int:id>', methods=['POST'])
@login_required
def irrigate(id):
    controller = IrrigationController.query.get_or_404(id)
    
    # Check if the controller belongs to the current user
    if controller.user_id != current_user.id:
        flash('You do not have permission to control this irrigation system', 'danger')
    else:
        controller.last_irrigation = datetime.utcnow()
        db.session.commit()
        flash(f'Irrigation triggered for {controller.name}!', 'success')
    
    return redirect(url_for('irrigation.list_controllers')) 