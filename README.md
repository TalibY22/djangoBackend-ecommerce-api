# Django E-commerce REST API

A robust e-commerce REST API built with Django REST Framework featuring user authentication, product management, shopping cart functionality, order processing, and payment integration.

## 🚀 Features

- User Authentication and Authorization
- Product Catalog Management
- Shopping Cart System
- Order Processing
- Wishlist Management
- Payment Integration
- Category Management
- Admin Dashboard

## 🛠️ Tech Stack

- Python 3.8+
- Django 4.0+
- Django REST Framework
- SQLite/PostgreSQL
- Token Authentication

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

## ⚙️ Installation & Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/ecommerce-api.git
cd ecommerce-api
```

2. **Create and activate virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
Create a `.env` file in the root directory:
```env
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=your-database-url
```

5. **Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Create superuser**
```bash
python manage.py createsuperuser
```

7. **Run development server**
```bash
python manage.py runserver
```

## 📝 API Documentation

### Authentication

The API uses token-based authentication. Include the token in the Authorization header:
```
Authorization: Token your-token-here
```

### API Endpoints

#### Customers
```http
# Register new customer
POST /api/customers/

# Get customer profile
GET /api/customers/{id}/

# Update customer profile
PUT /api/customers/{id}/
```

#### Products
```http
# List all products
GET /api/products/

# Get product details
GET /api/products/{id}/

# Filter products by category
GET /api/products/by_category/?category_id={id}
```

#### Cart Operations
```http
# Get user's cart
GET /api/cart/

# Add item to cart
POST /api/cart/{cart_id}/add_item/
{
    "product_id": "integer",
    "quantity": "integer"
}

# Remove item from cart
POST /api/cart/{cart_id}/remove_item/
{
    "product_id": "integer"
}
```

#### Orders
```http
# Create order from cart
POST /api/orders/create_from_cart/

# Get order details
GET /api/orders/{id}/
```

### Request & Response Examples

#### Creating a Customer
```http
POST /api/customers/
{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "phone_number": "1234567890",
    "address": "123 Main St",
    "dob": "1990-01-01"
}
```

Response:
```json
{
    "id": 1,
    "user": {
        "username": "john",
        "email": "john@example.com"
    },
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "1234567890",
    "address": "123 Main St",
    "dob": "1990-01-01"
}
```

## 🛒 Cart System Workflow

1. **Cart Creation**:
   - Automatic cart creation for new users
   - One active cart per user

2. **Adding Items**:
   - Add products with specified quantity
   - Automatic price calculation
   - Quantity validation

3. **Cart to Order Conversion**:
   - Create order from cart contents
   - Cart items transfer to order items
   - Cart cleared but preserved for future use

## 🔒 Security Features

- Token Authentication
- Permission-based access control
- Admin-only endpoints protection
- Input validation and sanitization
- Secure password handling

## 💡 Error Handling

The API uses standard HTTP status codes and returns detailed error messages:

```json
{
    "error": "string",
    "detail": "string",
    "status_code": "integer"
}
```

Common status codes:
- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `500`: Server Error

## 📊 Data Models

### Customer
```python
class customers(models.Model):
    user = models.OneToOneField(User)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField()
    phone_number = models.IntegerField()
    address = models.CharField(max_length=256)
    dob = models.DateField()
```

### Product
```python
class products(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    description = models.CharField(max_length=200)
    summary = models.CharField(max_length=200)
    SKU = models.IntegerField()
    category_type = models.ForeignKey(category)
```

[View all models](link-to-models-file)

## 🔄 Business Logic

### Cart Management
- Automatic cart creation
- Real-time total calculation
- Quantity management
- Empty cart validation

### Order Processing
- Cart to order conversion
- Order status management
- Payment integration
- Order history tracking

## 🛣️ Roadmap

- [ ] Payment Gateway Integration
- [ ] Product Reviews & Ratings
- [ ] User Dashboard
- [ ] Order Tracking
- [ ] Email Notifications
- [ ] Inventory Management

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## ✍️ Authors
TalibY22(https://github.com/TalibY22)

## 🙏 Acknowledgments

* Django REST Framework documentation
* Python community
* All contributors
