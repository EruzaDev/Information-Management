from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.models import Cart, Order, OrderItem, Review, Game
from app.forms.customer_forms import ShippingForm
from app import db

bp = Blueprint('customer', __name__)

@bp.route('/customer/dashboard')
@login_required
def dashboard():
    # Fetch orders for the logged-in customer
    orders = Order.query.filter_by(customer_id=current_user.id).order_by(Order.order_date.desc()).all()
    return render_template('customer/dashboard.html', orders=orders)

@bp.route('/cart')
@login_required
def cart():
    cart_items = Cart.query.filter_by(customer_id=current_user.id).all()
    total = sum(item.game.price * item.quantity for item in cart_items)
    return render_template('customer/cart.html', cart_items=cart_items, total=total)

@bp.route('/cart/add/<int:game_id>', methods=['POST'])
@login_required
def add_to_cart(game_id):
    quantity = int(request.form.get('quantity', 1))
    cart_item = Cart.query.filter_by(customer_id=current_user.id, game_id=game_id).first()
    game = Game.query.get_or_404(game_id)
    if quantity > game.stock_quantity:
        flash('Not enough stock available', 'danger')
        return redirect(url_for('main.game_detail', id=game_id))
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = Cart(customer_id=current_user.id, game_id=game_id, quantity=quantity)
        db.session.add(cart_item)
    db.session.commit()
    flash('Item added to cart', 'success')
    return redirect(url_for('customer.cart'))

@bp.route('/cart/update/<int:game_id>', methods=['POST'])
@login_required
def update_cart(game_id):
    quantity = int(request.form.get('quantity', 1))
    cart_item = Cart.query.filter_by(customer_id=current_user.id, game_id=game_id).first_or_404()
    game = Game.query.get_or_404(game_id)
    if quantity > game.stock_quantity:
        flash('Not enough stock available', 'danger')
        return redirect(url_for('customer.cart'))
    cart_item.quantity = quantity
    db.session.commit()
    flash('Cart updated', 'success')
    return redirect(url_for('customer.cart'))

@bp.route('/cart/remove/<int:game_id>', methods=['POST'])
@login_required
def remove_from_cart(game_id):
    cart_item = Cart.query.filter_by(customer_id=current_user.id, game_id=game_id).first_or_404()
    db.session.delete(cart_item)
    db.session.commit()
    flash('Item removed from cart', 'success')
    return redirect(url_for('customer.cart'))

@bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart_items = Cart.query.filter_by(customer_id=current_user.id).all()
    if not cart_items:
        flash('Your cart is empty', 'warning')
        return redirect(url_for('customer.cart'))
    
    total = sum(item.game.price * item.quantity for item in cart_items)
    
    if request.method == 'POST':
        shipping_address = request.form.get('shipping_address')
        phone_number = request.form.get('phone_number')
        special_instructions = request.form.get('special_instructions')
        
        if shipping_address and phone_number:  # Basic validation
            order = Order(
                customer_id=current_user.id,
                total_amount=total,
                status='pending'
            )
            db.session.add(order)
            db.session.flush()  # Get order.id
            
            for item in cart_items:
                order_item = OrderItem(
                    order_id=order.id,
                    game_id=item.game_id,
                    quantity=item.quantity,
                    price_at_time=item.game.price
                )
                db.session.add(order_item)
                # Reduce stock quantity
                item.game.stock_quantity -= item.quantity
                db.session.delete(item)  # Clear cart
            
            db.session.commit()
            flash('Order placed successfully', 'success')
            return redirect(url_for('customer.orders'))
        else:
            flash('Please fill in all required fields', 'danger')
    
    return render_template('customer/checkout.html', cart_items=cart_items, total=total)


@bp.route('/orders')
@login_required
def orders():
    orders = Order.query.filter_by(customer_id=current_user.id).order_by(Order.order_date.desc()).all()
    return render_template('customer/orders.html', orders=orders)

@bp.route('/orders/<int:order_id>')
@login_required
def order_detail(order_id):
    order = Order.query.filter_by(id=order_id, customer_id=current_user.id).first_or_404()
    return render_template('customer/order_detail.html', order=order)

@bp.route('/game/<int:game_id>/review', methods=['GET', 'POST'])
@login_required
def add_review(game_id):
    if request.method == 'POST':
        rating = request.form.get('rating')
        review_text = request.form.get('review_text')
        
        if rating and review_text:
            review = Review(
                customer_id=current_user.id,
                game_id=game_id,
                rating=int(rating),
                review_text=review_text
            )
            db.session.add(review)
            db.session.commit()
            flash('Review added', 'success')
            return redirect(url_for('main.game_detail', id=game_id))
        else:
            flash('Please fill in all fields', 'danger')
    
    return render_template('customer/add_review.html', game_id=game_id)

@bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone_number = request.form.get('phone_number')
        address = request.form.get('address')
        
        if all([name, email, phone_number, address]):
            current_user.name = name
            current_user.email = email
            current_user.phone_number = phone_number
            current_user.address = address
            db.session.commit()
            flash('Profile updated', 'success')
            return redirect(url_for('auth.profile'))
        else:
            flash('Please fill in all fields', 'danger')
    
    return render_template('auth/profile_edit.html')

@bp.route('/my_reviews')
@login_required
def my_reviews():
    reviews = Review.query.filter_by(customer_id=current_user.id).order_by(Review.review_date.desc()).all()
    return render_template('customer/my_reviews.html', reviews=reviews)
