// Checkout functionality
let cart = JSON.parse(localStorage.getItem('cart')) || [];

document.addEventListener('DOMContentLoaded', () => {
    renderOrderSummary();
    prefillUserData();
    setupFormSubmit();
});

// Prefill form fields from embedded user JSON (if available)
function prefillUserData() {
    try {
        const userEl = document.getElementById('user-data-json');
        if (!userEl) return;
        const user = JSON.parse(userEl.textContent || '{}');
        if (user.name) document.getElementById('name').value = user.name;
        if (user.email) document.getElementById('email').value = user.email;
        if (user.phone) document.getElementById('phone').value = user.phone;
        if (user.address) document.getElementById('address').value = user.address;
        if (user.city) document.getElementById('city').value = user.city;
    } catch (e) {
        console.warn('No user data to prefill');
    }
}

// Render order summary
function renderOrderSummary() {
    const orderItems = document.getElementById('order-items');
    const orderTotal = document.getElementById('order-total');

    orderItems.innerHTML = '';
    let total = 0;

    if (cart.length === 0) {
        orderItems.innerHTML = '<p style="padding: 1rem; text-align: center; color: #999;">No items in cart</p>';
        orderTotal.textContent = '0.00';
        return;
    }

    cart.forEach(item => {
        const itemTotal = item.price * item.quantity;
        total += itemTotal;

        const orderItem = document.createElement('div');
        orderItem.className = 'order-item';
        orderItem.innerHTML = `
            <span>${item.name} x ${item.quantity}</span>
            <span>Rs. ${itemTotal.toFixed(2)}</span>
        `;
        orderItems.appendChild(orderItem);
    });

    orderTotal.textContent = total.toFixed(2);
}

// Setup form submission
function setupFormSubmit() {
    const form = document.getElementById('checkout-form');
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        if (cart.length === 0) {
            alert('Your cart is empty!');
            return;
        }

        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;
        const phone = document.getElementById('phone').value;
        const address = document.getElementById('address').value;
        const city = document.getElementById('city').value;
        const notes = document.getElementById('notes').value;

        // Calculate total
        const totalPrice = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);

        const orderData = {
            customerDetails: {
                name,
                email,
                phone,
                address,
                city,
                notes
            },
            items: cart,
            totalPrice
        };

        try {
            const response = await fetch('/api/orders', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(orderData)
            });

            if (!response.ok) {
                throw new Error('Failed to place order');
            }

            const result = await response.json();

            if (result.success) {
                // Clear cart
                localStorage.removeItem('cart');
                
                // Redirect to success page
                window.location.href = `/success?order_id=${result.order_id}`;
            } else {
                alert('Error placing order: ' + (result.message || 'Unknown error'));
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Error placing order. Please try again.');
        }
    });
}
