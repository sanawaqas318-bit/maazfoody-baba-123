# MAAZ - Food Delivery Application

A modern Neobrutalist food delivery web application built with Flask and SQLite, featuring customer ordering and admin dashboard.

## Features

### Customer Features
- **Responsive Menu System**: Browse food items with category filtering (Main Courses, Appetizers, Desserts)
- **Shopping Cart**: Add/remove items, adjust quantities, persistent cart storage
- **Checkout Flow**: Collect customer details (name, phone, email, address, city, notes)
- **Order Placement**: Submit orders via API with automatic database storage
- **Success Page**: Order confirmation with Order ID

### Admin Features
- **Admin Authentication**: Secure login/registration with authorized email verification
- **Real-time Order Dashboard**: View all orders with live updates
- **Order Status Management**: Update order status (pending, approved, rejected)
- **Admin Statistics**: 
  - Total orders count
  - Pending orders count
  - Approved orders count
  - Rejected orders count
  - Total revenue tracking

### Design
- **Neobrutalist Aesthetic**: 
  - Yellow primary color (#ffca28)
  - 2px black borders throughout
  - Hard shadows for "pop" effect
  - PT Sans typography
- **Responsive Layout**: Mobile-first design with grid adapting to 2 columns on small screens
- **Animations**: 
  - Blur-text fade-in on hero section
  - Bounce cards for featured items
  - Smooth transitions and hover effects

## Project Structure

```
maaz/
├── app.py                 # Flask application and routes
├── requirements.txt       # Python dependencies
├── templates/            # HTML templates
│   ├── index.html       # Homepage with menu and cart
│   ├── checkout.html    # Checkout form page
│   ├── success.html     # Order success page
│   ├── admin_dashboard.html   # Admin panel
│   ├── admin_login.html       # Admin login page
│   ├── admin_register.html    # Admin registration page
│   ├── 404.html         # Not found error page
│   └── 500.html         # Server error page
├── static/
│   ├── css/
│   │   ├── style.css    # Main website styles
│   │   └── admin.css    # Admin panel styles
│   ├── js/
│   │   ├── script.js    # Main website scripts
│   │   ├── checkout.js  # Checkout page scripts
│   │   └── admin.js     # Admin dashboard scripts
│   └── images/          # Product images (placeholder support)
└── fooddelivery.db      # SQLite database (auto-created)
```

## Database Schema

### Users Table
- `id` (Integer, Primary Key)
- `email` (String, Unique)
- `password` (String, Hashed)
- `name` (String)
- `phone` (String)
- `address` (String)
- `role` (String)
- `created_at` (DateTime)

### Admin Table
- `id` (Integer, Primary Key)
- `email` (String, Unique)
- `password` (String, Hashed)
- `name` (String)
- `is_active` (Boolean)
- `created_at` (DateTime)

### MenuItem Table
- `id` (Integer, Primary Key)
- `name` (String)
- `category` (String)
- `description` (String)
- `price` (Float)
- `image_url` (String)
- `is_available` (Boolean)
- `created_at` (DateTime)

### Order Table
- `id` (Integer, Primary Key)
- `order_id` (String, Unique)
- `user_id` (Integer)
- `customer_name` (String)
- `customer_phone` (String)
- `customer_email` (String)
- `customer_address` (String)
- `customer_city` (String)
- `notes` (Text)
- `items` (JSON)
- `total_price` (Float)
- `order_status` (String)
- `created_at` (DateTime)
- `updated_at` (DateTime)

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Steps

1. **Navigate to project directory:**
   ```bash
   cd c:\Users\Waqas\Desktop\maaz
   ```

2. **Create virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python app.py
   ```

5. **Access the application:**
   - Homepage: http://localhost:5000
   - Admin Panel: http://localhost:5000/admin/login
   - Admin Registration: http://localhost:5000/admin/register

## Admin Account Setup

### Authorized Admin Emails
The system only allows registration for these email addresses:
- `arham.waqasahmed@gmail.com`
- `mnaeel381@gmail.com`

### First Admin Setup
1. Navigate to http://localhost:5000/admin/register
2. Enter one of the authorized emails
3. Create a password
4. Login with credentials

## API Endpoints

### Customer Endpoints

**GET /api/menu**
- Get all available menu items
- Query parameter: `category` (optional)
- Response: Array of menu items

**POST /api/orders**
- Create a new order
- Body: JSON with customerDetails, items, totalPrice
- Response: Order ID and confirmation message

**GET /api/orders/<order_id>**
- Get order details
- Response: Order information

### Admin Endpoints

**POST /admin/login**
- Admin login
- Body: email, password
- Response: Redirect to dashboard

**POST /admin/register**
- Register new admin (authorized emails only)
- Body: email, password, name
- Response: Success message

**GET /api/admin/orders**
- Get all orders (requires authentication)
- Response: Array of orders

**PATCH /api/admin/orders/<order_id>**
- Update order status (requires authentication)
- Body: status (pending/approved/rejected)
- Response: Updated order information

**GET /api/admin/stats**
- Get dashboard statistics (requires authentication)
- Response: Order counts and revenue

## Features Implemented

✅ Modern Neobrutalist UI with custom styling
✅ SQLite database with 4 models (Users, Admin, Menu Items, Orders)
✅ Shopping cart with persistent storage
✅ Order management system
✅ Admin authentication & authorization
✅ Real-time order dashboard
✅ Order status updates
✅ Revenue tracking
✅ Responsive mobile design
✅ Animations and transitions
✅ Error handling (404, 500)
✅ Database auto-initialization with sample data

## Default Menu Items

The application auto-populates with these items on first run:

**Main Courses:**
- Grilled Chicken Biryani (Rs. 450)
- Butter Chicken (Rs. 380)
- Beef Karahi (Rs. 520)

**Appetizers:**
- Samosas (Rs. 120)
- Chicken Tikka (Rs. 280)
- Seekh Kabab (Rs. 250)

**Desserts:**
- Gulab Jamun (Rs. 150)
- Kheer (Rs. 130)
- Jalebi (Rs. 100)

## Security Notes

⚠️ **Important**: Change the `SECRET_KEY` in `app.py` before deploying to production!

Default configuration is for development only. For production:
1. Use strong SECRET_KEY
2. Set Flask `debug=False`
3. Use environment variables for sensitive data
4. Enable HTTPS
5. Implement rate limiting
6. Use secure password hashing

## Troubleshooting

**Database Issues**
- Delete `fooddelivery.db` to reset the database
- Restart the Flask application

**Port Already in Use**
- Change port in `app.py`: `app.run(debug=True, port=5001)`

**Static Files Not Loading**
- Ensure static/ directory exists with css/ and js/ subdirectories
- Check browser console for 404 errors
- Restart Flask application

## Contact

**Restaurant Details:**
- Phone: 0324800263
- Address: 560 E-Block Sabzazar, Lahore

---

Built with Flask | Sqlite | Neobrutalist Design | 2026
