import sys
import os
sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..')))
from app import app, db, Admin
from werkzeug.security import generate_password_hash

USERNAME = 'arham'
PASSWORD = '1428'
EMAIL = 'arham.waqasahmed@gmail.com'
NAME = 'Arham'

with app.app_context():
    existing = Admin.query.filter_by(username=USERNAME).first()
    if existing:
        print('Admin already exists:', USERNAME)
    else:
        admin = Admin(username=USERNAME, email=EMAIL, name=NAME)
        admin.password = generate_password_hash(PASSWORD)
        db.session.add(admin)
        db.session.commit()
        print('Created admin:', USERNAME)
        print('Password:', PASSWORD)
