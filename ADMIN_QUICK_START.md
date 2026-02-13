# Admin Portal - Quick Start Guide

## ✅ Everything is Ready!

Your MAAZ Food Delivery admin portal is now fully operational and tested.

---

## 🚀 Getting Started (30 seconds)

### Step 1: Access Admin Login
Open your browser and go to:
```
http://localhost:5000/admin/login
```

### Step 2: Log In with Credentials
**Username:** `arham`  
**Password:** `1428`

### Step 3: View Dashboard
You'll see:
- Total orders count
- Pending orders count
- Approved orders count
- Rejected orders count
- Total revenue
- Total users

---

## 📋 Admin Features Available

### 1. **Dashboard** (Home)
- Real-time order statistics
- Recent orders list
- Update order status
- Track shipments

### 2. **Products** (`/admin/products`)
- Add new food items
- Edit existing products
- Delete products
- View all menu items

### 3. **Users** (`/admin/users`)
- View all registered customers
- See customer profiles
- Track signup dates

### 4. **Sales** (`/admin/sales`)
- View total revenue
- See all orders with revenue
- Calculate average order value
- Date-based analytics

### 5. **Announcements** (`/admin/announcements`)
- Post announcements to homepage
- Edit announcements
- Delete announcements
- Track creation dates

---

## 🔑 Your Admin Account

| Item | Details |
|------|---------|
| **Username** | arham |
| **Password** | 1428 |
| **Email** | arham.waqasahmed@gmail.com |
| **Name** | Arham |

---

## 💳 First Steps Inside Admin Portal

### 1. Add a Product
1. Click "📦 Products" in sidebar
2. Click "+ Add Product" button
3. Fill in:
   - Product Name (e.g., "Biryani")
   - Category (Main Courses, Appetizers, or Desserts)
   - Description
   - Price in Rs
4. Click "Save"
5. You'll see a success notification

### 2. View Orders
1. Click "📊 Dashboard" (homepage)
2. See all orders in the table
3. Click "Edit" button on any order
4. Update Status (pending → approved → rejected)
5. Update Tracking (Order Confirmed → Preparing → Ready → Delivered)
6. Click "Update"

### 3. Post Announcement
1. Click "📢 Announcements"
2. Click "+ Add Announcement"
3. Enter Title and Message
4. Click "Post"
5. Announcement appears on website homepage

### 4. Check Sales
1. Click "💰 Sales"
2. View:
   - Total Revenue
   - Total Orders
   - Average Order Value
3. See detailed order list below

### 5. View Users
1. Click "👥 Users"
2. See all registered customers
3. View their:
   - Email
   - Name
   - Phone
   - Address
   - Profile completion status

---

## 🎯 Common Tasks

### Update Order Status to "Approved"
```
1. Dashboard → Click "Edit" button on order
2. Order Status dropdown → Select "Approved"
3. Tracking Status → "Order Confirmed" or "Preparing"
4. Click "Update"
```

### Add New Food Item
```
1. Products → Click "+ Add Product"
2. Name: "Nihari"
3. Category: "Main Courses"
4. Description: "Traditional slow-cooked beef"
5. Price: "550"
6. Click "Save"
```

### Post New Announcement
```
1. Announcements → Click "+ Add Announcement"
2. Title: "20% OFF This Weekend!"
3. Message: "Get 20% discount on all orders..."
4. Click "Post"
```

---

## 🔐 Security Tips

✅ **Your session timeout:** 2 hours of inactivity  
✅ **Session cookie is secure:** Page refresh keeps you logged in  
✅ **Auto-logout available:** Click "🚪 Logout" when done  

### Best Practices:
- Use strong password (consider changing from 1428)
- Don't share login credentials
- Log out when done
- Clear cookies if login doesn't work

---

## 🆘 If Login Doesn't Work

### Quick Fix:
1. **Clear Cookies:**
   - Press `Ctrl + Shift + Delete`
   - Select "Cookies"
   - Click "Clear"

2. **Hard Refresh Page:**
   - Press `Ctrl + Shift + F5`
   - Try login again

3. **Use Incognito Mode:**
   - Open Private/Incognito window
   - Go to http://localhost:5000/admin/login
   - Login with arham / 1428

4. **Check Server:**
   - Ensure Flask is running
   - Should see messages in terminal

---

## 📊 Dashboard Explanation

### Statistics Cards:

| Card | Meaning |
|------|---------|
| **Total Orders** | All orders ever placed |
| **Pending** | Orders waiting for approval |
| **Approved** | Orders confirmed by admin |
| **Rejected** | Canceled orders |
| **Total Revenue** | Sum of all order totals |
| **Total Users** | Registered customers |

### Orders Table:

Shows all orders with:
- **Order ID:** Unique identifier
- **Customer:** Customer name
- **Phone:** Contact number
- **Items:** Number of items ordered
- **Total:** Amount in Rs.
- **Status:** Pending/Approved/Rejected
- **Tracking:** Delivery status
- **Date:** When ordered
- **Action:** Edit button to modify

---

## 🎨 Form Tips

### Adding Products
- **Name:** Keep it simple (e.g., "Chicken Tikka")
- **Category:** Must choose one of three
- **Description:** Optional but recommended
- **Price:** Enter numbers only (e.g., 450, not "Rs 450")

### Creating Announcements
- **Title:** Short header (e.g., "New Menu Items!")
- **Message:** Detailed announcement text
- **Max length:** Any length works

### Updating Orders
- **Status:** Pending → Approved → Rejected (one direction)
- **Tracking:** Can be updated independently
- **Options:** Predefined list to choose from

---

## 📱 Mobile Access

**Yes, admin portal works on mobile!**

1. Get server IP address from terminal
2. On mobile browser, go to: `http://<IP>:5000/admin/login`
3. Example: `http://192.168.1.100:5000/admin/login`
4. Login normally

---

## 🔗 Quick Links

| Feature | Link |
|---------|------|
| **Admin Login** | http://localhost:5000/admin/login |
| **Dashboard** | http://localhost:5000/admin |
| **Products** | http://localhost:5000/admin/products |
| **Users** | http://localhost:5000/admin/users |
| **Sales** | http://localhost:5000/admin/sales |
| **Announcements** | http://localhost:5000/admin/announcements |
| **Website** | http://localhost:5000 |

---

## 🔄 Session & Logout

### Session Stays Active:
- 2 hours of idle time
- Refreshes on page reload
- Survives browser refresh
- Stays until logout

### Logout:
1. Click "🚪 Logout" in sidebar
2. Returns to login page
3. Session is cleared
4. Need to login again

---

## ❓ FAQ

**Q: Can I change my password?**  
A: Currently, edit the database directly or recreate admin account with new password.

**Q: How many admins can I create?**  
A: Unlimited! Only authorized emails can register as admins.

**Q: Can I delete orders?**  
A: No, orders are permanent for records. You can change their status instead.

**Q: Can I backup the database?**  
A: Yes! File is at `instance/fooddelivery.db`. Keep copy of it for safety.

**Q: Is the data real?**  
A: Yes! All data is saved in SQLite database. It persists after restart.

---

## 🎓 Learning Resources

- See `ADMIN_LOGIN_FIX.md` for technical details
- See `INTEGRATION_GUIDE.md` for setup instructions
- See `FIXES_SUMMARY.md` for all improvements made

---

## ✅ Checklist for First Use

- [ ] Login with arham / 1428
- [ ] View dashboard statistics
- [ ] Add test product
- [ ] Post announcement
- [ ] View users list
- [ ] Check sales page
- [ ] Update order status
- [ ] Test logout

---

**Status:** ✅ Fully Operational  
**Last Updated:** February 11, 2026  
**Ready To Use:** YES ✅
