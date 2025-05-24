from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models.models import Cart, Game
from app import db

bp = Blueprint('ajax', __name__)

@bp.route('/api/cart/update/<int:game_id>', methods=['POST'])
@login_required
def update_cart(game_id):
    data = request.get_json()
    if data and 'quantity' in data:
        cart_item = Cart.query.filter_by(
            customer_id=current_user.id,
            game_id=game_id
        ).first_or_404()
        
        game = Game.query.get(game_id)
        quantity = int(data['quantity'])
        if quantity > game.stock_quantity:
            return jsonify({'error': 'Not enough stock available'}), 400
        
        cart_item.quantity = quantity
        db.session.commit()
        
        return jsonify({
            'success': True,
            'new_quantity': cart_item.quantity,
            'new_total': float(cart_item.quantity * game.price)
        })
    return jsonify({'error': 'Invalid form data'}), 400
