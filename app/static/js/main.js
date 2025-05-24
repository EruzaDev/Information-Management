document.addEventListener('DOMContentLoaded', function() {
    const quantityForms = document.querySelectorAll('.quantity-form');
    
    quantityForms.forEach(form => {
        const input = form.querySelector('.quantity-input');
        const decreaseBtn = form.querySelector('[data-action="decrease"]');
        const increaseBtn = form.querySelector('[data-action="increase"]');
        const gameId = form.dataset.gameId;
        
        // Update quantity when buttons are clicked
        decreaseBtn.addEventListener('click', () => updateQuantity(input, -1, gameId));
        increaseBtn.addEventListener('click', () => updateQuantity(input, 1, gameId));
        
        // Update quantity when input changes
        input.addEventListener('change', () => {
            const value = parseInt(input.value);
            const max = parseInt(input.max);
            const min = parseInt(input.min);
            
            if (value > max) {
                input.value = max;
                alert('Maximum available quantity is ' + max);
            } else if (value < min) {
                input.value = min;
            }
            
            updateCart(gameId, input.value);
        });
    });
    
    function updateQuantity(input, change, gameId) {
        const currentValue = parseInt(input.value);
        const newValue = currentValue + change;
        const max = parseInt(input.max);
        const min = parseInt(input.min);
        
        if (newValue <= max && newValue >= min) {
            input.value = newValue;
            updateCart(gameId, newValue);
        }
    }
    
    function updateCart(gameId, quantity) {
        fetch(`/api/cart/update/${gameId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ quantity: quantity })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
                return;
            }
            
            // Update subtotal for this item
            const cartItem = document.querySelector(`[data-game-id="${gameId}"]`).closest('.cart-item');
            const subtotal = cartItem.querySelector('.subtotal');
            subtotal.textContent = `$${data.new_total.toFixed(2)}`;
            
            // Update total
            updateOrderSummary();
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while updating the cart');
        });
    }
    
    function updateOrderSummary() {
        const subtotals = Array.from(document.querySelectorAll('.subtotal'))
            .map(el => parseFloat(el.textContent.replace('$', '')));
        const total = subtotals.reduce((a, b) => a + b, 0);
        
        document.getElementById('subtotal').textContent = `$${total.toFixed(2)}`;
        document.getElementById('total').textContent = `$${total.toFixed(2)}`;
    }
});
