import sys
import os
sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..')))
from app import app

# Create a test client
client = app.test_client()

print("=" * 60)
print("Testing Admin Login Flow")
print("=" * 60)

# Step 1: GET login page
print("\n1. Getting /admin/login page...")
response = client.get('/admin/login')
print(f"   Status: {response.status_code}")

# Step 2: POST login credentials
print("\n2. Posting login credentials (arham / 1428)...")
response = client.post('/admin/login', data={
    'username': 'arham',
    'password': '1428'
})
print(f"   Status: {response.status_code}")
print(f"   Location: {response.location if response.status_code == 302 else 'N/A'}")

# Step 3: Follow redirect to admin dashboard
if response.status_code == 302:
    print("\n3. Following redirect to dashboard...")
    response = client.get(response.location)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print("   ✅ Dashboard loaded successfully!")
    elif response.status_code == 302:
        print(f"   ⚠️  Another redirect occurred to: {response.location}")
        # Try one more time
        response = client.get(response.location)
        print(f"   Status: {response.status_code}")

print("\n" + "=" * 60)
print("Test Complete")
print("=" * 60)
