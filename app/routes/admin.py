from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, login_user, current_user
from app.models.models import Game, Genre, Order, Customer, Employee
from app.forms.admin_forms import AdminLoginForm, AdminChangePasswordForm
from app import db

bp = Blueprint('admin', __name__)

@bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    form = AdminLoginForm()
    if form.validate_on_submit():
        # Check employee table for admin login
        employee = Employee.query.filter_by(email=form.email.data).first()
        if employee is None:
            # If not found in employee, check customer table (optional)
            from app.models.models import Customer
            customer = Customer.query.filter_by(email=form.email.data).first()
            if customer:
                flash('Invalid admin credentials', 'danger')
            else:
                flash('Invalid email or password', 'danger')
            return render_template('auth/admin_login.html', form=form)
        else:
            # Verify password here if password validation is implemented
            login_user(employee)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('admin.dashboard'))
    return render_template('auth/admin_login.html', form=form)

@bp.after_app_request
def add_debug_current_user(response):
    from flask_login import current_user
    import logging
    logging.debug(f"Current user after request: {current_user} (type: {type(current_user)})")
    return response

@bp.route('/admin/dashboard')
@login_required
def dashboard():
    total_orders = Order.query.count()
    total_customers = Customer.query.count()
    total_games = Game.query.count()
    low_stock = Game.query.filter(Game.stock_quantity < 5).all()
    recent_orders = Order.query.order_by(Order.order_date.desc()).limit(5).all()
    return render_template('admin/dashboard.html',
                           total_orders=total_orders,
                           total_customers=total_customers,
                           total_games=total_games,
                           low_stock=low_stock,
                           recent_orders=recent_orders)

@bp.route('/admin/orders')
@login_required
def orders():
    orders = Order.query.order_by(Order.order_date.desc()).all()
    return render_template('admin/orders.html', orders=orders)

@bp.route('/admin/customers')
@login_required
def customers():
    customers = Customer.query.order_by(Customer.name).all()
    return render_template('admin/customers.html', customers=customers)

@bp.route('/admin/customers/add', methods=['GET', 'POST'])
@login_required
def add_customer():
    from app.forms.admin_forms import CustomerForm
    form = CustomerForm()
    if form.validate_on_submit():
        new_customer = Customer(
            name=form.name.data,
            email=form.email.data,
            phone_number=form.phone_number.data,
            address=form.address.data
        )
        if form.password.data:
            new_customer.set_password(form.password.data)
        db.session.add(new_customer)
        db.session.commit()
        flash('Customer added successfully!', 'success')
        return redirect(url_for('admin.customers'))
    return render_template('admin/add_customer.html', form=form)

@bp.route('/admin/customers/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_customer(id):
    from app.forms.admin_forms import CustomerForm
    customer = Customer.query.get_or_404(id)
    form = CustomerForm(obj=customer)
    if form.validate_on_submit():
        customer.name = form.name.data
        customer.email = form.email.data
        customer.phone_number = form.phone_number.data
        customer.address = form.address.data
        if form.password.data:
            customer.set_password(form.password.data)
        db.session.commit()
        flash('Customer updated successfully!', 'success')
        return redirect(url_for('admin.customers'))
    return render_template('admin/edit_customer.html', form=form, customer=customer)

@bp.route('/admin/customers/delete/<int:id>', methods=['POST'])
@login_required
def delete_customer(id):
    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    flash('Customer deleted successfully!', 'success')
    return redirect(url_for('admin.customers'))

@bp.route('/admin/games/add', methods=['GET', 'POST'])
@login_required
def add_game():
    from app.forms.admin_forms import GameForm
    from app.models.models import Game, Genre
    form = GameForm()
    # Populate genre choices
    genres = Genre.query.all()
    form.genre_id.choices = [(g.id, g.name) for g in genres]

    if form.validate_on_submit():
        new_game = Game(
            title=form.title.data,
            release_year=form.release_year.data,
            description=form.description.data,
            stock_quantity=form.stock_quantity.data,
            price=form.price.data,
            image_url=form.image_url.data,
            genre_id=form.genre_id.data
        )
        db.session.add(new_game)
        db.session.commit()
        flash('Game added successfully!', 'success')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/add_game.html', form=form)

@bp.route('/admin/games/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_game(id):
    from app.forms.admin_forms import GameForm
    game = Game.query.get_or_404(id)
    form = GameForm(obj=game)
    genres = Genre.query.all()
    form.genre_id.choices = [(g.id, g.name) for g in genres]

    if form.validate_on_submit():
        game.title = form.title.data
        game.release_year = form.release_year.data
        game.description = form.description.data
        game.stock_quantity = form.stock_quantity.data
        game.price = form.price.data
        game.image_url = form.image_url.data
        game.genre_id = form.genre_id.data
        db.session.commit()
        flash('Game updated successfully!', 'success')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/edit_game.html', form=form, game=game)

@bp.route('/admin/games/delete/<int:id>', methods=['POST'])
@login_required
def delete_game(id):
    game = Game.query.get_or_404(id)
    db.session.delete(game)
    db.session.commit()
    flash('Game deleted successfully!', 'success')
    return redirect(url_for('admin.dashboard'))

@bp.route('/admin/genres/add', methods=['GET', 'POST'])
@login_required
def add_genre():
    from app.forms.admin_forms import GenreForm
    form = GenreForm()
    if form.validate_on_submit():
        from app.models.models import Genre
        new_genre = Genre(name=form.name.data)
        db.session.add(new_genre)
        db.session.commit()
        flash('Genre added successfully!', 'success')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/add_genre.html', form=form)

@bp.route('/admin/genres/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_genre(id):
    from app.forms.admin_forms import GenreForm
    from app.models.models import Genre
    genre = Genre.query.get_or_404(id)
    form = GenreForm(obj=genre)
    if form.validate_on_submit():
        genre.name = form.name.data
        db.session.commit()
        flash('Genre updated successfully!', 'success')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/edit_genre.html', form=form, genre=genre)

@bp.route('/admin/orders/<int:id>/status', methods=['POST'])
@login_required
def update_order_status(id):
    order = Order.query.get_or_404(id)
    new_status = request.form.get('status')
    if new_status in ['pending', 'completed', 'cancelled']:
        order.status = new_status
        db.session.commit()
        flash('Order status updated successfully!', 'success')
    else:
        flash('Invalid status value.', 'danger')
    return redirect(url_for('admin.orders'))

@bp.route('/admin/orders/<int:id>')
@login_required
def order_detail(id):
    order = Order.query.get_or_404(id)
    return render_template('admin/order_detail.html', order=order)

@bp.route('/admin/employees/add', methods=['GET', 'POST'])
@login_required
def add_employee():
    from app.forms.admin_forms import EmployeeForm
    form = EmployeeForm()
    if form.validate_on_submit():
        from app.models.models import Employee
        new_employee = Employee(
            name=form.name.data,
            email=form.email.data,
            position=form.position.data,
            role=form.role.data
        )
        if form.password.data:
            new_employee.set_password(form.password.data)
        db.session.add(new_employee)
        db.session.commit()
        flash('Employee added successfully!', 'success')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/add_employee.html', form=form)

@bp.route('/admin/employees/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_employee(id):
    from app.forms.admin_forms import EmployeeForm
    from app.models.models import Employee
    employee = Employee.query.get_or_404(id)
    form = EmployeeForm(obj=employee)
    if form.validate_on_submit():
        employee.name = form.name.data
        employee.email = form.email.data
        employee.position = form.position.data
        employee.role = form.role.data
        if form.password.data:
            employee.set_password(form.password.data)
        db.session.commit()
        flash('Employee updated successfully!', 'success')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/edit_employee.html', form=form, employee=employee)
