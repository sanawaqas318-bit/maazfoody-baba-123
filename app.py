from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
import json
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fooddelivery.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True only for HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = 7200  # 2 hours
app.config['SESSION_REFRESH_EACH_REQUEST'] = True
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True
app.config['GOOGLE_CLIENT_ID'] = os.environ.get('GOOGLE_CLIENT_ID', 'your-google-client-id')
app.config['GOOGLE_CLIENT_SECRET'] = os.environ.get('GOOGLE_CLIENT_SECRET', 'your-google-client-secret')

# OAuth setup (Google)
oauth = OAuth(app)
oauth.register(
    name='google',
    client_id=app.config['GOOGLE_CLIENT_ID'],
    client_secret=app.config['GOOGLE_CLIENT_SECRET'],
    access_token_url='https://oauth2.googleapis.com/token',
    authorize_url='https://accounts.google.com/o/oauth2/v2/auth',
    api_base_url='https://www.googleapis.com/oauth2/v2/',
    userinfo_endpoint='https://www.googleapis.com/oauth2/v3/userinfo',
    client_kwargs={'scope': 'openid email profile'},
)

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'user_login'


@app.before_request
def make_session_permanent():
    session.permanent = True


# Admin emails
ADMIN_EMAILS = ['arham.waqasahmed@gmail.com', 'mnaeel381@gmail.com']

# Database Models
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    country = db.Column(db.String(50))
    province = db.Column(db.String(50))
    address = db.Column(db.String(255))
    profile_complete = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255))
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(255))
    is_available = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(50), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    customer_name = db.Column(db.String(120), nullable=False)
    customer_phone = db.Column(db.String(20), nullable=False)
    customer_email = db.Column(db.String(120), nullable=False)
    customer_address = db.Column(db.String(255), nullable=False)
    customer_city = db.Column(db.String(50), nullable=False)
    notes = db.Column(db.Text)
    items = db.Column(db.JSON, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    order_status = db.Column(db.String(20), default='pending')
    tracking_status = db.Column(db.String(100), default='Order Confirmed')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_by = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Frontend Routes
@app.route('/')
def index():
    announcements = Announcement.query.filter_by(is_active=True).order_by(Announcement.created_at.desc()).all()
    return render_template('index.html', announcements=announcements)


@app.route('/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            return render_template('user_login.html', error='Invalid credentials')
    
    return render_template('user_login.html')


@app.route('/auth/google')
def auth_google():
    redirect_uri = url_for('auth_google_callback', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@app.route('/auth/google/callback')
def auth_google_callback():
    try:
        token = oauth.google.authorize_access_token()
    except Exception:
        return redirect(url_for('user_login'))

    resp = oauth.google.get('userinfo')
    user_info = resp.json()
    email = user_info.get('email')
    name = user_info.get('name') or (email.split('@')[0] if email else None)

    if not email:
        return redirect(url_for('user_login'))

    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(email=email, name=name)
        # assign a random password since login will use OAuth
        user.set_password(os.urandom(16).hex())
        db.session.add(user)
        db.session.commit()

    login_user(user)
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def user_register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            return render_template('user_register.html', error='Passwords do not match')
        
        if User.query.filter_by(email=email).first():
            return render_template('user_register.html', error='Email already registered')
        
        user = User(email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        return redirect(url_for('user_profile'))
    
    return render_template('user_register.html')


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def user_profile():
    if request.method == 'POST':
        current_user.name = request.form.get('name')
        current_user.phone = request.form.get('phone')
        current_user.country = request.form.get('country')
        current_user.province = request.form.get('province')
        current_user.address = request.form.get('address')
        
        if all([current_user.name, current_user.phone, current_user.country, 
                current_user.province, current_user.address]):
            current_user.profile_complete = True
        
        db.session.commit()
        return redirect(url_for('user_orders'))
    
    return render_template('user_profile.html', user=current_user)


@app.route('/orders')
@login_required
def user_orders():
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('user_orders.html', orders=orders)


@app.route('/order-detail/<order_id>')
@login_required
def order_detail(order_id):
    order = Order.query.filter_by(order_id=order_id).first()
    if not order or order.user_id != current_user.id:
        return render_template('404.html'), 404
    return render_template('order_detail.html', order=order)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/checkout')
def checkout():
    if not current_user.is_authenticated:
        return redirect(url_for('user_login'))
    if not current_user.profile_complete:
        return redirect(url_for('user_profile'))
    return render_template('checkout.html', user=current_user)


@app.route('/success')
def success():
    return render_template('success.html')


# API Routes
@app.route('/api/menu', methods=['GET'])
def get_menu():
    category = request.args.get('category')
    if category:
        items = MenuItem.query.filter_by(category=category, is_available=True).all()
    else:
        items = MenuItem.query.filter_by(is_available=True).all()
    
    return jsonify([{
        'id': item.id,
        'name': item.name,
        'category': item.category,
        'description': item.description,
        'price': item.price,
        'image_url': item.image_url
    } for item in items])


@app.route('/api/menu', methods=['POST'])
def add_menu_item():
    data = request.json
    item = MenuItem(
        name=data['name'],
        category=data['category'],
        description=data.get('description'),
        price=data['price'],
        image_url=data.get('image_url')
    )
    db.session.add(item)
    db.session.commit()
    return jsonify({'id': item.id, 'message': 'Item added'})


@app.route('/api/orders', methods=['POST'])
def create_order():
    data = request.json
    from uuid import uuid4
    
    user_id = None
    if current_user.is_authenticated:
        user_id = current_user.id
    
    order = Order(
        order_id=str(uuid4())[:8].upper(),
        user_id=user_id,
        customer_name=data['customerDetails']['name'],
        customer_phone=data['customerDetails']['phone'],
        customer_email=data['customerDetails']['email'],
        customer_address=data['customerDetails']['address'],
        customer_city=data['customerDetails']['city'],
        notes=data['customerDetails'].get('notes'),
        items=data['items'],
        total_price=data['totalPrice']
    )
    
    db.session.add(order)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'order_id': order.order_id,
        'message': 'Order placed successfully'
    })


@app.route('/api/orders/<order_id>', methods=['GET'])
def get_order(order_id):
    order = Order.query.filter_by(order_id=order_id).first()
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    
    return jsonify({
        'id': order.id,
        'order_id': order.order_id,
        'customer_name': order.customer_name,
        'items': order.items,
        'total_price': order.total_price,
        'order_status': order.order_status,
        'created_at': order.created_at.isoformat()
    })


# Admin Routes
@app.route('/admin')
def admin_dashboard():
    admin = None
    if 'admin_id' in session:
        admin = Admin.query.get(session['admin_id'])
    
    if not admin:
        return redirect(url_for('admin_login'))
    
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('admin_dashboard.html', orders=orders, admin=admin)


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        admin = Admin.query.filter_by(username=username).first()
        
        if admin and admin.check_password(password):
            session.permanent = True
            session['admin_id'] = admin.id
            session['admin_username'] = admin.username
            session['admin_name'] = admin.name
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('admin_login.html', error='Invalid credentials')
    
    if 'admin_id' in session:
        return redirect(url_for('admin_dashboard'))
    
    return render_template('admin_login.html')


@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_id', None)
    return redirect(url_for('admin_login'))


@app.route('/admin/register', methods=['GET', 'POST'])
def admin_register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')
        
        if email not in ADMIN_EMAILS:
            return render_template('admin_register.html', error='Email not authorized for admin registration')
        
        if Admin.query.filter_by(username=username).first():
            return render_template('admin_register.html', error='Username already exists')
        
        if Admin.query.filter_by(email=email).first():
            return render_template('admin_register.html', error='Email already registered')
        
        admin = Admin(username=username, email=email, name=name)
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()
        
        return redirect(url_for('admin_login'))
    
    return render_template('admin_register.html')


@app.route('/admin/users')
def admin_users():
    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))
    
    users = User.query.all()
    return render_template('admin_users.html', users=users)


@app.route('/admin/products')
def admin_products():
    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))
    
    items = MenuItem.query.all()
    return render_template('admin_products.html', items=items)


@app.route('/admin/sales')
def admin_sales():
    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))
    
    orders = Order.query.all()
    return render_template('admin_sales.html', orders=orders)


@app.route('/admin/announcements')
def admin_announcements():
    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))
    
    announcements = Announcement.query.all()
    return render_template('admin_announcements.html', announcements=announcements)


@app.route('/api/admin/products', methods=['POST'])
def add_product():
    if 'admin_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.json
    item = MenuItem(
        name=data['name'],
        category=data['category'],
        description=data.get('description'),
        price=data['price'],
        image_url=data.get('image_url')
    )
    db.session.add(item)
    db.session.commit()
    return jsonify({'success': True, 'id': item.id})


@app.route('/api/admin/products/<int:item_id>', methods=['PUT'])
def update_product(item_id):
    if 'admin_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    item = MenuItem.query.get(item_id)
    if not item:
        return jsonify({'error': 'Product not found'}), 404
    
    data = request.json
    item.name = data.get('name', item.name)
    item.category = data.get('category', item.category)
    item.description = data.get('description', item.description)
    item.price = data.get('price', item.price)
    item.is_available = data.get('is_available', item.is_available)
    
    db.session.commit()
    return jsonify({'success': True})


@app.route('/api/admin/products/<int:item_id>', methods=['DELETE'])
def delete_product(item_id):
    if 'admin_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    item = MenuItem.query.get(item_id)
    if not item:
        return jsonify({'error': 'Product not found'}), 404
    
    db.session.delete(item)
    db.session.commit()
    return jsonify({'success': True})


@app.route('/api/admin/announcements', methods=['POST'])
def add_announcement():
    if 'admin_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.json
    announcement = Announcement(
        title=data['title'],
        message=data['message'],
        created_by=session['admin_id']
    )
    db.session.add(announcement)
    db.session.commit()
    return jsonify({'success': True, 'id': announcement.id})


@app.route('/api/admin/announcements/<int:ann_id>', methods=['PUT'])
def update_announcement(ann_id):
    if 'admin_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    announcement = Announcement.query.get(ann_id)
    if not announcement:
        return jsonify({'error': 'Announcement not found'}), 404
    
    data = request.json
    announcement.title = data.get('title', announcement.title)
    announcement.message = data.get('message', announcement.message)
    db.session.commit()
    return jsonify({'success': True, 'id': announcement.id})


@app.route('/api/admin/announcements/<int:ann_id>', methods=['DELETE'])
def delete_announcement(ann_id):
    if 'admin_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    announcement = Announcement.query.get(ann_id)
    if not announcement:
        return jsonify({'error': 'Announcement not found'}), 404
    
    db.session.delete(announcement)
    db.session.commit()
    return jsonify({'success': True})


@app.route('/api/admin/orders/<int:order_id>', methods=['PATCH'])
def update_order_status(order_id):
    if 'admin_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.json
    order = Order.query.get(order_id)
    
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    
    order.order_status = data.get('status', order.order_status)
    order.tracking_status = data.get('tracking_status', order.tracking_status)
    order.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({
        'success': True,
        'order_id': order.order_id,
        'status': order.order_status
    })


@app.route('/api/admin/stats', methods=['GET'])
def get_admin_stats():
    if 'admin_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    total_orders = Order.query.count()
    pending_orders = Order.query.filter_by(order_status='pending').count()
    approved_orders = Order.query.filter_by(order_status='approved').count()
    rejected_orders = Order.query.filter_by(order_status='rejected').count()
    total_revenue = db.session.query(db.func.sum(Order.total_price)).scalar() or 0
    total_users = User.query.count()
    total_products = MenuItem.query.count()
    
    return jsonify({
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'approved_orders': approved_orders,
        'rejected_orders': rejected_orders,
        'total_revenue': float(total_revenue),
        'total_users': total_users,
        'total_products': total_products
    })


@app.route('/api/admin/users', methods=['GET'])
def get_all_users():
    if 'admin_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    users = User.query.all()
    return jsonify([{
        'id': user.id,
        'email': user.email,
        'name': user.name,
        'phone': user.phone,
        'country': user.country,
        'province': user.province,
        'address': user.address,
        'profile_complete': user.profile_complete,
        'created_at': user.created_at.isoformat()
    } for user in users])


@app.route('/api/admin/orders', methods=['GET'])
def get_all_orders():
    if 'admin_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return jsonify([{
        'id': order.id,
        'order_id': order.order_id,
        'customer_name': order.customer_name,
        'customer_phone': order.customer_phone,
        'items': order.items,
        'total_price': order.total_price,
        'order_status': order.order_status,
        'tracking_status': order.tracking_status,
        'created_at': order.created_at.isoformat()
    } for order in orders])


# Error handlers
@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Create default menu items if not exists
        if MenuItem.query.count() == 0:
            menu_items = [
                MenuItem(name='Grilled Chicken Biryani', category='Main Courses', description='Fragrant basmati rice with tender grilled chicken', price=450.00, image_url='biryani.jpg'),
                MenuItem(name='Butter Chicken', category='Main Courses', description='Creamy tomato-based curry with succulent chicken pieces', price=380.00, image_url='butter_chicken.jpg'),
                MenuItem(name='Beef Karahi', category='Main Courses', description='Tender beef cooked in a traditional karahi with fresh peppers', price=520.00, image_url='beef_karahi.jpg'),
                MenuItem(name='Samosas', category='Appetizers', description='Crispy fried pastries filled with spiced potatoes and peas', price=120.00, image_url='samosas.jpg'),
                MenuItem(name='Chicken Tikka', category='Appetizers', description='Marinated chicken pieces grilled to perfection', price=280.00, image_url='tikka.jpg'),
                MenuItem(name='Seekh Kabab', category='Appetizers', description='Minced meat kababs with aromatic spices', price=250.00, image_url='seekh.jpg'),
                MenuItem(name='Gulab Jamun', category='Desserts', description='Soft milk solids in sugar syrup with cardamom', price=150.00, image_url='gulab.jpg'),
                MenuItem(name='Kheer', category='Desserts', description='Traditional rice pudding with nuts and dried fruits', price=130.00, image_url='kheer.jpg'),
                MenuItem(name='Jalebi', category='Desserts', description='Crispy spirals soaked in sugar syrup', price=100.00, image_url='jalebi.jpg'),
            ]
            for item in menu_items:
                db.session.add(item)
            db.session.commit()
    
    app.run(debug=True, port=5000)
