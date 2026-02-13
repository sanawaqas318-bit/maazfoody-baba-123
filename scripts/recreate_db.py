import sys
import os
sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..')))
from app import app, db, MenuItem

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'instance', 'fooddelivery.db')
DB_PATH = os.path.normpath(DB_PATH)

with app.app_context():
    # Remove existing DB file if present
    if os.path.exists(DB_PATH):
        os.rename(DB_PATH, DB_PATH + '.bak')
        print('Backed up existing DB to', DB_PATH + '.bak')

    db.create_all()

    # Seed default menu items if none exist
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
        print('Seeded default menu items')

    print('Database recreated and ready')
