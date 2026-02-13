# MAAZ Food Delivery - Integration & Setup Guide

## 📋 System Requirements

- Python 3.8 or higher
- Windows/Mac/Linux
- 100MB disk space
- SQLite (included with Python)

## 🚀 Installation Steps

### Step 1: Clone/Download Project
```bash
cd c:\Users\Waqas\Desktop\folder
```

### Step 2: Create Virtual Environment
```bash
python -m venv .venv
```

### Step 3: Activate Virtual Environment

**Windows (PowerShell):**
```powershell
.\.venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
.venv\Scripts\activate.bat
```

**Mac/Linux:**
```bash
source .venv/bin/activate
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Initialize Database
```bash
python scripts/recreate_db.py
```

### Step 6: Create Admin Account
```bash
python scripts/setup_arham_admin.py
```

Or create your own admin:
```bash
python scripts/create_admin.py
```

### Step 7: Run Application
```bash
python app.py
```

The application will start at: **http://localhost:5000**

---

## 📱 Access Points

| Page | URL |
|------|-----|
| **Homepage** | http://localhost:5000 |
| **User Login** | http://localhost:5000/login |
| **User Register** | http://localhost:5000/register |
| **Admin Login** | http://localhost:5000/admin/login |
| **Admin Register** | http://localhost:5000/admin/register |
| **Admin Dashboard** | http://localhost:5000/admin |

---

## 👥 Default Admin Account

| Field | Value |
|-------|-------|
| **Username** | arham |
| **Password** | 1428 |
| **Email** | arham.waqasahmed@gmail.com |

---

## 📦 Dependencies Explained

| Package | Version | Purpose |
|---------|---------|---------|
| Flask | 3.0.0 | Web framework |
| Flask-SQLAlchemy | 3.1.1 | Database ORM |
| Flask-Login | 0.6.3 | User authentication |
| Flask-Cors | 4.0.0 | Cross-origin requests |
| Werkzeug | 3.0.1 | WSGI utilities & password hashing |
| python-dotenv | 1.0.0 | Environment variables |
| SQLAlchemy | 2.0.23 | Database toolkit |

---

## 🔐 Admin Authorized Emails

Only these emails can register as admins:
- arham.waqasahmed@gmail.com
- mnaeel381@gmail.com

To add more authorized emails, edit `app.py` line 20:
```python
ADMIN_EMAILS = ['arham.waqasahmed@gmail.com', 'mnaeel381@gmail.com', 'newemail@example.com']
```

---

## 📊 Database

- **Type:** SQLite
- **Location:** `instance/fooddelivery.db`
- **Backup:** `instance/fooddelivery.db.bak`

### Tables:
- `admin` - Admin user accounts
- `user` - Customer user accounts
- `menu_item` - Food items/products
- `order` - Customer orders
- `announcement` - Admin announcements

---

## 🎯 Features Overview

### Customer Features
✅ Browse food menu  
✅ Filter by category  
✅ Add items to cart  
✅ User registration & login  
✅ Complete profile  
✅ Place orders  
✅ Track orders  
✅ View order history  

### Admin Features
✅ Secure admin login  
✅ Dashboard with statistics  
✅ Manage products (Add/Edit/Delete)  
✅ View all customers  
✅ Manage orders (Status updates)  
✅ View sales & revenue  
✅ Post announcements  
✅ Real-time order updates  

---

## 🐛 Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'flask'`
**Solution:** Ensure virtual environment is activated and dependencies are installed
```bash
pip install -r requirements.txt
```

### Issue: Port 5000 already in use
**Solution:** Change port in `app.py` last line:
```python
app.run(debug=True, port=5001)  # Change 5000 to 5001
```

### Issue: Database locked error
**Solution:** Delete `fooddelivery.db` and recreate:
```bash
python scripts/recreate_db.py
```

### Issue: Login form fields disappearing when typing
**Solution:** This has been fixed in the latest version. Clear browser cache (Ctrl+Shift+Delete) and refresh.

---

## 📝 Environment Configuration

Create `.env` file (optional) for production:
```
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-production-secret-key
DATABASE_URL=sqlite:///fooddelivery.db
```

---

## 🚢 Production Deployment

### Using Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Security Checklist:
- [ ] Change `SECRET_KEY` in `app.py`
- [ ] Set `debug=False` in production
- [ ] Use environment variables for sensitive data
- [ ] Update authorized admin emails
- [ ] Set up proper database backups
- [ ] Enable HTTPS/SSL certificate

---

## 📞 Support Files

| File | Purpose |
|------|---------|
| `app.py` | Main Flask application |
| `requirements.txt` | Python dependencies |
| `scripts/recreate_db.py` | Initialize/reset database |
| `scripts/create_admin.py` | Create new admin account |
| `scripts/setup_arham_admin.py` | Setup default admin |
| `templates/` | HTML pages |
| `static/css/` | Stylesheets |
| `static/js/` | JavaScript files |

---

## 🎨 Design System

- **Color Scheme:** Neobrutalist
- **Primary Color:** #ffca28 (Yellow)
- **Typography:** PT Sans
- **Borders:** 2px solid black
- **Shadows:** Hard shadows for depth

---

## 📞 Quick Commands

```bash
# Activate environment
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Initialize database
python scripts/recreate_db.py

# Create admin user
python scripts/setup_arham_admin.py

# Run application
python app.py

# Deactivate environment
deactivate
```

---

**Last Updated:** February 11, 2026  
**Version:** 1.0.0  
**Status:** Ready for Production
