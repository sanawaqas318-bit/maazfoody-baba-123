// Cart Management
let cart = JSON.parse(localStorage.getItem('cart')) || [];

// Load menu items on page load
document.addEventListener('DOMContentLoaded', () => {
    loadMenu('all');
    updateCartCount();
    animateBlurText();
});

// Animate blur text on load
function animateBlurText() {
    const blurText = document.querySelector('.blur-text');
    if (!blurText) return;

    const text = blurText.textContent;
    const words = text.split(' ');
    blurText.textContent = '';

    words.forEach((word, index) => {
        const span = document.createElement('span');
        span.textContent = word + ' ';
        span.style.animation = `slideUp 0.6s ease-out ${index * 0.1 + 0.3}s both`;
        blurText.appendChild(span);
    });
}

// Load menu items from API
async function loadMenu(category) {
    try {
        const url = category === 'all' ? '/api/menu' : `/api/menu?category=${category}`;
        const response = await fetch(url);
        const items = await response.json();

        const menuGrid = document.getElementById('menu-grid');
        menuGrid.innerHTML = '';

        items.forEach(item => {
            const card = document.createElement('div');
            card.className = 'menu-item';
            card.innerHTML = `
                <img src="${item.image_url || 'https://via.placeholder.com/280x200?text=' + encodeURIComponent(item.name)}" 
                     alt="${item.name}" class="menu-item-image" onerror="this.src='https://via.placeholder.com/280x200?text=${encodeURIComponent(item.name)}'">
                <div class="menu-item-content">
                    <h3>${item.name}</h3>
                    <p>${item.description}</p>
                    <div class="menu-item-price">Rs. ${item.price.toFixed(2)}</div>
                    <button class="btn-add-cart" onclick="addToCart(${item.id}, '${item.name}', ${item.price})">
                        Add to Cart
                    </button>
                </div>
            `;
            menuGrid.appendChild(card);
        });
    } catch (error) {
        console.error('Error loading menu:', error);
    }
}

// Filter menu by category
function filterMenu(category) {
    const buttons = document.querySelectorAll('.filter-btn');
    buttons.forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');

    loadMenu(category);
}

// Add item to cart
function addToCart(id, name, price) {
    const existingItem = cart.find(item => item.id === id);

    if (existingItem) {
        existingItem.quantity++;
    } else {
        cart.push({
            id,
            name,
            price,
            quantity: 1
        });
    }

    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartCount();
    showNotification(`${name} added to cart!`);
}

// Open cart modal
function openCart() {
    const modal = document.getElementById('cart-modal');
    modal.classList.add('active');
    renderCartItems();
}

// Close cart modal
function closeCart() {
    const modal = document.getElementById('cart-modal');
    modal.classList.remove('active');
}

// Render cart items
function renderCartItems() {
    const cartItems = document.getElementById('cart-items');
    cartItems.innerHTML = '';

    if (cart.length === 0) {
        cartItems.innerHTML = '<p style="text-align: center; color: #999;">Your cart is empty</p>';
        document.getElementById('cart-total').textContent = '0.00';
        return;
    }

    let total = 0;

    cart.forEach(item => {
        const itemTotal = item.price * item.quantity;
        total += itemTotal;

        const cartItem = document.createElement('div');
        cartItem.className = 'cart-item';
        cartItem.innerHTML = `
            <div class="cart-item-info">
                <div class="cart-item-name">${item.name}</div>
                <div class="cart-item-price">Rs. ${item.price.toFixed(2)}</div>
            </div>
            <div class="cart-item-quantity">
                <button class="qty-btn" onclick="updateQuantity(${item.id}, -1)">-</button>
                <span>${item.quantity}</span>
                <button class="qty-btn" onclick="updateQuantity(${item.id}, 1)">+</button>
            </div>
            <button class="remove-btn" onclick="removeFromCart(${item.id})">Remove</button>
        `;
        cartItems.appendChild(cartItem);
    });

    document.getElementById('cart-total').textContent = total.toFixed(2);
}

// Update item quantity
function updateQuantity(id, change) {
    const item = cart.find(item => item.id === id);
    if (item) {
        item.quantity += change;
        if (item.quantity <= 0) {
            removeFromCart(id);
        } else {
            localStorage.setItem('cart', JSON.stringify(cart));
            renderCartItems();
        }
    }
}

// Remove item from cart
function removeFromCart(id) {
    cart = cart.filter(item => item.id !== id);
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartCount();
    renderCartItems();
}

// Update cart count
function updateCartCount() {
    const count = cart.reduce((total, item) => total + item.quantity, 0);
    document.getElementById('cart-count').textContent = count;
}

// Proceed to checkout
function proceedToCheckout() {
    if (cart.length === 0) {
        alert('Your cart is empty!');
        return;
    }
    window.location.href = '/checkout';
}

// Show notification
function showNotification(message) {
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        background-color: #51cf66;
        color: white;
        padding: 1rem 1.5rem;
        border: 2px solid #000;
        border-radius: 4px;
        z-index: 1000;
        animation: slideIn 0.3s ease-out;
        font-weight: 600;
    `;
    notification.textContent = message;
    document.body.appendChild(notification);

    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    }, 2000);
}

// Close modal when clicking outside
window.addEventListener('click', (event) => {
    const modal = document.getElementById('cart-modal');
    if (event.target === modal) {
        closeCart();
    }
});

// Add styles for notifications
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }

    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// ==================== FADE-IN BEHAVIOR ====================
(function(){
    document.addEventListener('DOMContentLoaded', () => {
        const selectors = 'section, main, .container, .content, .card, .panel, .menu-item, .hero-inner';
        const nodes = Array.from(document.querySelectorAll(selectors));
        nodes.forEach((el, i) => {
            el.classList.add('fade-in');
            el.style.setProperty('--fade-delay', `${i * 60}ms`);
            // small stagger so content comes in sequence
            setTimeout(() => el.classList.add('visible'), 50 + i * 60);
        });
    });
})();

// ==================== TILT EFFECT ====================
(function(){
    if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

    function initTilt(selector, opts = {}){
        const max = opts.max || 12;
        const scale = opts.scale || 1.02;
        const els = document.querySelectorAll(selector);
        els.forEach(el => {
            el.classList.add('tilt');
            const onMove = (e) => {
                const clientX = e.clientX || (e.touches && e.touches[0] && e.touches[0].clientX);
                const clientY = e.clientY || (e.touches && e.touches[0] && e.touches[0].clientY);
                if (clientX == null) return;
                const r = el.getBoundingClientRect();
                const dx = clientX - (r.left + r.width/2);
                const dy = clientY - (r.top + r.height/2);
                const px = dx / (r.width/2);
                const py = dy / (r.height/2);
                const rotY = px * max;
                const rotX = -py * max;
                el.style.transform = `perspective(800px) rotateX(${rotX}deg) rotateY(${rotY}deg) scale(${scale})`;
            };
            const onLeave = () => { el.style.transform = ''; };
            el.addEventListener('pointermove', onMove);
            el.addEventListener('pointerleave', onLeave);
            el.addEventListener('touchmove', onMove, {passive:true});
            el.addEventListener('touchend', onLeave);
        });
    }

    document.addEventListener('DOMContentLoaded', () => {
        initTilt('.menu-item, .card, .stat-card, .menu-grid .menu-item, .menu-item-image, .btn-hero, .btn-primary');
    });
})();
