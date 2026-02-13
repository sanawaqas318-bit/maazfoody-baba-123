import sys
import os
import json
sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..')))
from app import app, db, User, MenuItem, Order
from werkzeug.security import generate_password_hash

with app.app_context():
    # create test user
    email = 'testuser@example.com'
    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(email=email, name='Test User', phone='03001234567', country='Pakistan', province='Punjab', address='123 Test St', profile_complete=True)
        user.set_password('testpass')
        db.session.add(user)
        db.session.commit()
        print('Created test user:', email)
    else:
        print('Test user exists')

    # Prepare items from menu
    items = []
    menu_items = MenuItem.query.limit(2).all()
    for m in menu_items:
        items.append({'id': m.id, 'name': m.name, 'price': m.price, 'quantity': 1})

    if not items:
        print('No menu items to create order')
        sys.exit(0)

    # create order
    from uuid import uuid4
    order = Order(
        order_id=str(uuid4())[:8].upper(),
        user_id=user.id,
        customer_name=user.name,
        customer_phone=user.phone,
        customer_email=user.email,
        customer_address=user.address,
        customer_city=user.province,
        notes='Test order created by script',
        items=items,
        total_price=sum(i['price']*i['quantity'] for i in items)
    )
    db.session.add(order)
    db.session.commit()
    print('Created test order:', order.order_id)
