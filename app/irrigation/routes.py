"""Irrigation control routes."""

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

from app.models import IrrigationController
from app.core.extensions import db
from . import irrigation
from datetime import datetime


class IrrigationControllerForm(FlaskForm):
    """Form for irrigation controller creation and editing."""
    name = StringField('Nome do Controlador', validators=[DataRequired(), Length(min=3, max=100)])
    moisture_level = FloatField('Nível de Umidade (%)', validators=[DataRequired(), NumberRange(min=0, max=100)])
    is_active = BooleanField('Ativo')
    submit = SubmitField('Salvar')


@irrigation.route('/list')
@login_required
def list_controllers():
    """List irrigation controllers for current user."""
    controllers = IrrigationController.query.filter_by(user_id=current_user.id).all()
    return render_template('irrigation/list.html', title='Controladores de Irrigação', controllers=controllers)


@irrigation.route('/add', methods=['GET', 'POST'])
@login_required
def add_controller():
    """Add new irrigation controller."""
    form = IrrigationControllerForm()
    if form.validate_on_submit():
        controller = IrrigationController(
            name=form.name.data,
            user_id=current_user.id,
            moisture_level=form.moisture_level.data
        )
        controller.is_active = form.is_active.data
        db.session.add(controller)
        db.session.commit()
        flash('Controlador de irrigação criado com sucesso!', 'success')
        return redirect(url_for('irrigation.list_controllers'))
    return render_template('irrigation/form.html', title='Adicionar Controlador', form=form)


@irrigation.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_controller(id):
    """Edit existing irrigation controller."""
    controller = IrrigationController.query.get_or_404(id)
    
    # Check if the controller belongs to the current user
    if controller.user_id != current_user.id:
        flash('Você não tem permissão para editar este controlador', 'danger')
        return redirect(url_for('irrigation.list_controllers'))
    
    form = IrrigationControllerForm()
    
    if form.validate_on_submit():
        controller.name = form.name.data
        controller.moisture_level = form.moisture_level.data
        controller.is_active = form.is_active.data
        
        db.session.commit()
        flash('Controlador de irrigação atualizado com sucesso!', 'success')
        return redirect(url_for('irrigation.list_controllers'))
        
    elif request.method == 'GET':
        form.name.data = controller.name
        form.moisture_level.data = controller.moisture_level
        form.is_active.data = controller.is_active
    
    return render_template('irrigation/form.html', title='Editar Controlador', form=form)


@irrigation.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_controller(id):
    """Delete irrigation controller."""
    controller = IrrigationController.query.get_or_404(id)
    
    # Check if the controller belongs to the current user
    if controller.user_id != current_user.id:
        flash('Você não tem permissão para deletar este controlador', 'danger')
    else:
        db.session.delete(controller)
        db.session.commit()
        flash('Controlador de irrigação deletado com sucesso!', 'success')
    
    return redirect(url_for('irrigation.list_controllers'))


@irrigation.route('/irrigate/<int:id>', methods=['POST'])
@login_required
def irrigate(id):
    """Trigger irrigation for a specific controller."""
    controller = IrrigationController.query.get_or_404(id)
    
    # Check if the controller belongs to the current user
    if controller.user_id != current_user.id:
        flash('Você não tem permissão para controlar este sistema de irrigação', 'danger')
    else:
        controller.irrigate()  # Use the model method
        db.session.commit()
        flash(f'Irrigação acionada para {controller.name}!', 'success')
    
    return redirect(url_for('irrigation.list_controllers')) 