from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models.models import Customer, Employee
from app.forms.auth_forms import (CustomerRegistrationForm, CustomerLoginForm, 
                                EmployeeLoginForm, ChangePasswordForm)
from app import db

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = CustomerRegistrationForm()
    if form.validate_on_submit():
        customer = Customer(
            name=form.name.data,
            email=form.email.data,
            phone_number=form.phone_number.data,
            address=form.address.data
        )
        customer.set_password(form.password.data)
        
        try:
            db.session.add(customer)
            db.session.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash('Registration failed. Please try again.', 'danger')
            
    return render_template('auth/register.html', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = CustomerLoginForm()
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        customer = Customer.query.filter_by(email=email).first()
        if customer and customer.check_password(password):
            login_user(customer)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('customer.dashboard'))
        flash('Invalid email or password', 'danger')
        
    return render_template('auth/login.html', form=form)



@bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    
    form = EmployeeLoginForm()
    if form.validate_on_submit():
        employee = Employee.query.filter_by(email=form.email.data).first()
        if employee:
            # Remove password validation, allow login if user exists
            login_user(employee)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('admin.dashboard'))
        flash('Invalid email or password', 'danger')
        
    return render_template('auth/admin_login.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.check_password(form.current_password.data):
            current_user.set_password(form.new_password.data)
            db.session.commit()
            flash('Your password has been updated.', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid current password.', 'danger')
    return render_template('auth/change_password.html', form=form)

@bp.route('/profile')
@login_required
def profile():
    return render_template('auth/profile.html')
