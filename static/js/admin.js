// Admin Dashboard functionality
let currentOrderId = null;

document.addEventListener('DOMContentLoaded', () => {
    loadOrders();
    loadStats();

    // Refresh data every 30 seconds
    setInterval(() => {
        loadOrders();
        loadStats();
    }, 30000);
});

// Load all orders
async function loadOrders() {
    try {
        const response = await fetch('/api/admin/orders');
        if (!response.ok) {
            if (response.status === 401) {
                window.location.href = '/admin/login';
                return;
            }
            throw new Error('Failed to load orders');
        }

        const orders = await response.json();
        renderOrdersTable(orders);
    } catch (error) {
        console.error('Error loading orders:', error);
    }
}

// Load statistics
async function loadStats() {
    try {
        const response = await fetch('/api/admin/stats');
        if (!response.ok) throw new Error('Failed to load stats');

        const stats = await response.json();

        document.getElementById('stat-total').textContent = stats.total_orders;
        document.getElementById('stat-pending').textContent = stats.pending_orders;
        document.getElementById('stat-approved').textContent = stats.approved_orders;
        document.getElementById('stat-rejected').textContent = stats.rejected_orders;
        document.getElementById('stat-revenue').textContent = 'Rs. ' + stats.total_revenue.toFixed(2);
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

// Render orders in table
function renderOrdersTable(orders) {
    const tbody = document.getElementById('orders-body');
    tbody.innerHTML = '';

    if (orders.length === 0) {
        tbody.innerHTML = '<tr><td colspan="9" style="text-align: center; padding: 2rem;">No orders yet</td></tr>';
        return;
    }

    orders.forEach(order => {
        const date = new Date(order.created_at).toLocaleDateString() + ' ' + 
                     new Date(order.created_at).toLocaleTimeString();
        
        const itemsCount = order.items.length;
        
        let statusClass = 'status-pending';
        if (order.order_status === 'approved') statusClass = 'status-approved';
        if (order.order_status === 'rejected') statusClass = 'status-rejected';

        const row = document.createElement('tr');
        row.innerHTML = `
            <td><strong>${order.order_id}</strong></td>
            <td>${order.customer_name}</td>
            <td>${order.customer_phone}</td>
            <td>${itemsCount} item(s)</td>
            <td>Rs. ${order.total_price.toFixed(2)}</td>
            <td><span class="status-badge ${statusClass}">${order.order_status.toUpperCase()}</span></td>
            <td><small>${order.tracking_status}</small></td>
            <td>${date}</td>
            <td><button class="btn-edit" onclick="openStatusModal(${order.id}, '${order.order_id}', '${order.order_status}')">Edit</button></td>
        `;
        tbody.appendChild(row);
    });
}

// Open status update modal
function openStatusModal(orderId, orderIdStr, currentStatus) {
    currentOrderId = orderId;
    document.getElementById('modal-order-id').textContent = `Order ID: ${orderIdStr}`;
    document.getElementById('status-select').value = currentStatus;
    
    const modal = document.getElementById('status-modal');
    modal.classList.add('active');
}

// Close status modal
function closeStatusModal() {
    const modal = document.getElementById('status-modal');
    modal.classList.remove('active');
    currentOrderId = null;
}

// Update order status
async function updateOrderStatus() {
    const newStatus = document.getElementById('status-select').value;
    const trackingStatus = document.getElementById('tracking-select').value;

    try {
        const response = await fetch(`/api/admin/orders/${currentOrderId}`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ status: newStatus, tracking_status: trackingStatus })
        });

        if (!response.ok) throw new Error('Failed to update order status');

        const result = await response.json();
        
        if (result.success) {
            closeStatusModal();
            loadOrders();
            loadStats();
            showNotification(`Order ${result.order_id} updated!`);
        } else {
            throw new Error(result.error || 'Failed to update order');
        }
    } catch (error) {
        console.error('Error updating order:', error);
        showNotification('Error: ' + error.message, 'error');
    }
}

// Show notification
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    const bgColor = type === 'error' ? '#ff6b6b' : '#51cf66';
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        background-color: ${bgColor};
        color: white;
        padding: 1rem 1.5rem;
        border: 2px solid #000;
        box-shadow: 6px 6px 0px rgba(0, 0, 0, 0.3);
        z-index: 1000;
        animation: slideIn 0.3s ease-out;
        font-weight: 600;
        font-family: 'PT Sans', sans-serif;
    `;
    notification.textContent = message;
    document.body.appendChild(notification);

    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Close modal when clicking outside
window.addEventListener('click', (event) => {
    const modal = document.getElementById('status-modal');
    if (event.target === modal) {
        closeStatusModal();
    }
});

// Refresh orders function
function refreshOrders() {
    loadOrders();
    loadStats();
}

// Search functionality for orders
const searchOrders = document.getElementById('searchOrders');
if (searchOrders) {
    searchOrders.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        const rows = document.querySelectorAll('#orders-body tr');
        
        rows.forEach(row => {
            const text = row.textContent.toLowerCase();
            row.style.display = text.includes(searchTerm) ? '' : 'none';
        });
    });
}

// Add animation styles
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

// ==================== FADE-IN BEHAVIOR (ADMIN) ====================
(function(){
    document.addEventListener('DOMContentLoaded', () => {
        const selectors = 'section, main, .admin-main, .admin-container, .auth-box, .admin-header, .stat-card, .orders-section';
        const nodes = Array.from(document.querySelectorAll(selectors));
        nodes.forEach((el, i) => {
            el.classList.add('fade-in');
            el.style.setProperty('--fade-delay', `${i * 50}ms`);
            setTimeout(() => el.classList.add('visible'), 50 + i * 50);
        });
    });
})();

// ==================== TILT EFFECT (ADMIN) ====================
(function(){
    if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

    function initTilt(selector, opts = {}){
        const max = opts.max || 10;
        const scale = opts.scale || 1.015;
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
        initTilt('.stat-card, .menu-item, .orders-section .stat-card, .btn-edit, .admin-header');
    });
})();
