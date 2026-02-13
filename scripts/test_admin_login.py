import sys
import os
sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..')))
from app import app, db, Admin

with app.app_context():
    # Check if admin exists
    admin = Admin.query.filter_by(username='arham').first()
    
    if admin:
        print("✅ Admin user found:")
        print(f"   Username: {admin.username}")
        print(f"   Email: {admin.email}")
        print(f"   Name: {admin.name}")
        print(f"   ID: {admin.id}")
        
        # Test password
        if admin.check_password('1428'):
            print("✅ Password is correct!")
        else:
            print("❌ Password is incorrect!")
    else:
        print("❌ Admin user 'arham' not found!")
        print("\nAll admins in database:")
        all_admins = Admin.query.all()
        for a in all_admins:
            print(f"  - {a.username} ({a.email})")
