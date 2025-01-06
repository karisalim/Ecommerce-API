# Ecommerce API 🛒

A robust and scalable e-commerce backend built with Django and Django REST Framework (DRF). This project provides APIs for user authentication, product management, and order processing.

## 🔧 Technologies Used
- **Backend**: Django, Django REST Framework (DRF)
- **Database**: SQLite (Development), PostgreSQL (Production-ready)
- **Authentication**: JWT (JSON Web Tokens)
- **API Documentation**: Swagger/OpenAPI
- **Testing**: Django Testing Framework
- **Version Control**: Git, GitHub

## 🔄 Setup Instructions
1. **Clone the repository**:
   ```bash
   git clone https://github.com/karisalim/Ecommerce-API.git
   cd Ecommerce-API
   ```
2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Run migrations**:
   ```bash
   python manage.py migrate
   ```
5. **Start the development server**:
   ```bash
   python manage.py runserver
   ```
6. **Access the admin panel**:
   Go to [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) (Credentials: user: karim, pass: 123456789)

## 🔀 Project Structure
```
emarket/
├── account/
│   ├── migrations/
│   │   ├── 0001_initial.py
│   │   ├── 0002_alter_profile_reset_password_token.py
│   │   └── __init__.py
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── emarket/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── order/
│   ├── migrations/
│   │   ├── 0001_initial.py
│   │   ├── 0002_alter_orderitem_order.py
│   │   └── __init__.py
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── product/
│   ├── migrations/
│   │   ├── 0001_initial.py
│   │   ├── 0002_rename_createat_product_created_at_and_updated_at.py
│   │   ├── 0003_review.py
│   │   ├── 0004_alter_review_ratings.py
│   │   └── __init__.py
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── filters.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── utils/
│   └── error_view.py
├── db.sqlite3
└── manage.py
```

## 🔄 Features

### **Product Management**
- **CRUD operations**: Create, Read, Update, and Delete products and categories.
- **Filtering**: Filter products by price, brand, and category.
- **Search**: Search for products by name or description.
- **Sorting**: Sort products by price, rating, or creation date.

### **Authentication & Authorization**
- **User registration**: Register new users with email, password, and personal details.
- **User login**: Login using email and password to receive JWT tokens.
- **Token-based authentication**: Secure API endpoints using JWT tokens.

### **Order Management**
- **Create orders**: Add products to the cart and create orders.
- **Order tracking**: Track the status of orders (e.g., pending, shipped, delivered).
- **Order history**: View past orders and their details.

### **Scalable Design**
- **Modular structure**: Easily extend the project with new features like payments, shipping, and reviews.
- **API documentation**: Integrated Swagger/OpenAPI for easy API exploration.


## 🔐 Authentication

This API uses **Token-based Authentication** to secure endpoints. Follow these steps to authenticate:

1. **Register a new user**:
   - Send a `POST` request to `/api/register/` with your username, email, and password.
   - Example:
     ```json
     {
       "username": "testuser",
       "email": "test@example.com",
       "password": "password123"
     }
     ```

2. **Login and get your token**:
   - Send a `POST` request to `/api/token/` with your username and password.
   - Example:
     ```json
     {
       "username": "testuser",
       "password": "password123"
     }
     ```
   - You will receive a response with **access** and **refresh** tokens:
     ```json
     {
       "refresh": "your-refresh-token",
       "access": "your-access-token"
     }
     ```

3. **Use the token**:
   - Include the **access token** in the `Authorization` header for all protected endpoints.
   - Example:
     ```
     Authorization: Bearer your-access-token
     ```

4. **Refresh your token**:
   - If your access token expires, send a `POST` request to `/api/token/refresh/` with your **refresh token**.
   - Example:
     ```json
     {
       "refresh": "your-refresh-token"
     }
     ```

---

### إضافة مثال لاستخدام الـ Token في الـ **Endpoints**:

```markdown
## 🚀 API Endpoints

### **Orders**
- **GET `/api/orders/`**: Get all orders.
  - **Headers**:
    ```
    Authorization: Bearer your-access-token
    ```
  - **Response**:
    ```json
    [
      {
        "id": 1,
        "status": "Pending",
        "products": [
          {
            "id": 1,
            "name": "Product 1",
            "quantity": 2
          }
        ]
      }
    ]
    ```

- **POST `/api/orders/new/`**: Create a new order.
  - **Headers**:
    ```
    Authorization: Bearer your-access-token
    ```
  - **Request Body**:
    ```json
    {
      "products": [
        {
          "id": 1,
          "quantity": 2
        }
      ]
    }
    ```

- **PUT `/api/orders/<id>/process/`**: Update the status of an order.
  - **Headers**:
    ```
    Authorization: Bearer your-access-token
    ```
  - **Request Body**:
    ```json
    {
      "status": "Shipped"
    }
    ```

- **DELETE `/api/orders/delete/`**: Delete an order.
  - **Headers**:
    ```
    Authorization: Bearer your-access-token
    ```