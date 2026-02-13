import sys
import os
sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..')))
from app import app, db, Admin

USERNAME = 'arham'
PASSWORD = '1428'
EMAIL = 'arham.waqasahmed@gmail.com'
NAME = 'Arham'

with app.app_context():
    # Delete existing admin with this email if it exists
    existing = Admin.query.filter_by(email=EMAIL).first()
    if existing:
        db.session.delete(existing)
        db.session.commit()
        print('Deleted existing admin with email:', EMAIL)
    
    # Create new admin with specified credentials
    admin = Admin(username=USERNAME, email=EMAIL, name=NAME)
    admin.set_password(PASSWORD)
    db.session.add(admin)
    db.session.commit()
    print('✅ Admin Created Successfully')
    print('Username:', USERNAME)
    print('Password:', PASSWORD)
    print('Email:', EMAIL)
