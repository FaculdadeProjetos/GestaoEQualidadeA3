from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, BooleanField, SubmitField, DateTimeField
from wtforms.validators import DataRequired, Length, NumberRange, Optional
from datetime import datetime

from app.models import IrrigationController, IrrigationSchedule, IrrigationHistory
from app import db

irrigation = Blueprint('irrigation', __name__)

class IrrigationControllerForm(FlaskForm):
    name = StringField('Controller Name', validators=[DataRequired(), Length(min=3, max=100)])
    moisture_level = FloatField('Moisture Level (%)', validators=[DataRequired(), NumberRange(min=0, max=100)])
    is_active = BooleanField('Active')
    submit = SubmitField('Save')

class IrrigationScheduleForm(FlaskForm):
    start_time = DateTimeField('Start Time', validators=[DataRequired()])
    duration_minutes = FloatField('Duration (min)', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Schedule')

@irrigation.route('/irrigation')
@login_required
def list_controllers():
    controllers = IrrigationController.query.filter_by(user_id=current_user.id).all()
    return render_template('irrigation/list.html', controllers=controllers)

@irrigation.route('/irrigation/add', methods=['GET', 'POST'])
@login_required
def add_controller():
    form = IrrigationControllerForm()
    if form.validate_on_submit():
        try:
            controller = IrrigationController(
                name=form.name.data,
                moisture_level=form.moisture_level.data,
                is_active=form.is_active.data,
                user_id=current_user.id
            )
            db.session.add(controller)
            db.session.commit()
            flash('Controller added successfully.', 'success')
            return redirect(url_for('irrigation.list_controllers'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding controller: {str(e)}', 'danger')
    return render_template('irrigation/add.html', form=form)

@irrigation.route('/irrigation/schedule/<int:controller_id>', methods=['GET', 'POST'])
@login_required
def schedule_irrigation(controller_id):
    form = IrrigationScheduleForm()
    if form.validate_on_submit():
        try:
            schedule = IrrigationSchedule(
                controller_id=controller_id,
                start_time=form.start_time.data,
                duration_minutes=form.duration_minutes.data
            )
            db.session.add(schedule)
            db.session.commit()
            flash('Irrigation scheduled successfully.', 'success')
            return redirect(url_for('irrigation.list_controllers'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error scheduling irrigation: {str(e)}', 'danger')
    return render_template('irrigation/schedule.html', form=form)

@irrigation.route('/irrigation/history')
@login_required
def view_history():
    history = IrrigationHistory.query.join(IrrigationController).filter(
        IrrigationController.user_id == current_user.id
    ).order_by(IrrigationHistory.timestamp.desc()).all()
    return render_template('irrigation/history.html', history=history)