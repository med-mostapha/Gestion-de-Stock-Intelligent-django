# 📦 Gestion de Stock Intelligent API  
**Stock Management • Alert System • Secure REST Architecture**

A secure and scalable Django REST API for managing:

- Users  
- Categories  
- Products  
- Stock thresholds  
- Expiration alerts  

Designed to be:# 📦 Gestion de Stock Intelligent API  
**Stock Management • Alert System • Secure REST Architecture**

A secure and scalable Django REST API for managing:

- Users  
- Categories  
- Products  
- Stock thresholds  
- Expiration alerts  

Designed to be:

- Secure by default  
- User-isolated  
- Frontend-friendly  
- Cleanly structured  
- Easily extensible  

---

# 🎯 Project Objectives

- 🔐 Secure authentication  
- 📦 User-owned product management  
- 📂 Category-based organization  
- ⚠️ Automatic low stock detection  
- ⏳ Expired product alerts  
- 🔒 Strict user-level data isolation  
- 🧱 Clean RESTful architecture  

---

# 🏗️ Architecture Overview

Each user owns:

- Multiple categories  
- Multiple products (inside categories)

### Data relationship

```
User
 └── Category (owner = user)
      └── Product (category → owner)
```

All queries are filtered by:

```python
category__owner=request.user
```

This guarantees no cross-user data access.

---

# 🔐 Authentication

All protected endpoints require authentication.

### Header format (Token)

```
Authorization: Token <your_token>
```

### OR (JWT)

```
Authorization: Bearer <your_access_token>
```

---

# 🌍 Base API URL

```
/api/
```

---

# 👤 AUTHENTICATION ENDPOINTS

## 📝 Register  
**POST** `/api/register/`

### Request
```json
{
  "username": "mohamed",
  "email": "mohamed@email.com",
  "password": "StrongPassword123"
}
```

### Response
```json
{
  "id": 1,
  "username": "mohamed",
  "email": "mohamed@email.com"
}
```

---

## 🔑 Login  
**POST** `/api/login/`

### Request
```json
{
  "username": "mohamed",
  "password": "StrongPassword123"
}
```

### Response
```json
{
  "token": "your_auth_token_here"
}
```

Store token in:

- LocalStorage (simple apps)  
- HTTP-only cookies (recommended for production)  

---

# 📂 CATEGORY ENDPOINTS

Categories belong to the authenticated user.

## 📋 List Categories  
**GET** `/api/categories/`

### Response
```json
[
  {
    "id": 1,
    "name": "Electronics",
    "created_at": "2026-02-10T10:00:00Z"
  }
]
```

## ➕ Create Category  
**POST** `/api/categories/`

```json
{
  "name": "Food"
}
```

## ✏️ Update Category  
**PATCH** `/api/categories/{id}/`

## ❌ Delete Category  
**DELETE** `/api/categories/{id}/`

---

# 📦 PRODUCT ENDPOINTS

Products belong to categories.  
Categories belong to users.  
Products are always user-scoped.

## 📋 List Products  
**GET** `/api/products/`

## 🔍 Retrieve Product  
**GET** `/api/products/{id}/`

## ➕ Create Product  
**POST** `/api/products/`

```json
{
  "name": "Laptop",
  "price": "1200.00",
  "quantity": 10,
  "min_threshold": 3,
  "expiration_date": "2026-12-31",
  "category": 2
}
```

## ✏️ Update Product  
**PATCH** `/api/products/{id}/`

Example:

```json
{
  "quantity": 2
}
```

## ❌ Delete Product  
**DELETE** `/api/products/{id}/`

---

# ⚠️ ALERT SYSTEM

**GET** `/api/products/alerts/`  
Authentication required.

Returns:

- `low_stock`
- `expired`

---

## 🔎 Low Stock Definition

A product is low stock if:

```
quantity <= min_threshold
```

Uses Django `F()` expressions for database-level comparison.

---

## ⏳ Expired Definition

A product is expired if:

```
expiration_date IS NOT NULL
AND expiration_date <= today
```

Date comparison uses timezone-aware server logic.

---

## Example Response

```json
{
  "low_stock": [
    {
      "id": 2,
      "name": "Laptop",
      "price": "1200.00",
      "quantity": 2,
      "min_threshold": 3,
      "expiration_date": null,
      "category": 2,
      "is_low_stock": true,
      "has_expiry": false,
      "created_at": "2026-02-17T11:58:58.098847Z"
    }
  ],
  "expired": [
    {
      "id": 5,
      "name": "Milk",
      "price": "2.50",
      "quantity": 10,
      "min_threshold": 2,
      "expiration_date": "2020-01-01",
      "category": 1,
      "is_low_stock": false,
      "has_expiry": true,
      "created_at": "2026-02-10T08:00:00Z"
    }
  ]
}
```

---

# 🧠 Product Object Reference

| Field | Type | Description |
|-------|------|------------|
| id | Integer | Primary key |
| name | String | Product name |
| price | Decimal | Product price |
| quantity | Integer | Current stock |
| min_threshold | Integer | Alert threshold |
| expiration_date | Date (nullable) | Expiry date |
| category | Integer | Category ID |
| created_at | DateTime | Creation timestamp |
| is_low_stock | Boolean | Computed field |
| has_expiry | Boolean | True if expiration_date exists |

---

# 🔒 Security Model

- All endpoints (except register/login) require authentication  
- Products filtered by category ownership  
- Categories filtered by owner  
- No direct product-user relation exposed  
- Backend enforces ownership rules  

---

# 🖥️ Frontend Integration Reference

## Typical Dashboard Flow

1. Login → store token  
2. Fetch categories  
3. Fetch products  
4. Fetch alerts  
5. Render dashboard widgets  

## Suggested Dashboard Widgets

- Total Products  
- Total Categories  
- Low Stock Count  
- Expired Products Count  

Use:

```
GET /api/products/alerts/
```

to populate notification badges.

---

# 🧪 How to Trigger Alerts (Testing)

## Trigger Low Stock

```json
{
  "quantity": 2,
  "min_threshold": 3
}
```

## Trigger Expired

```json
{
  "expiration_date": "2020-01-01"
}
```

---

# 📦 Installation (Backend)

```bash
git clone <repository-url>
cd Gestion-de-Stock-Intelligent-django

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
```

---

# 🛠️ Possible Future Enhancements

- Pagination  
- Search & filtering  
- Sales tracking  
- Stock movement history  
- Email alerts  
- Admin dashboard  
- Role-based permissions  
- Docker deployment  
- CI/CD pipeline  

---

# 🏁 Conclusion

This API provides:

- Clean REST structure  
- Secure user isolation  
- Alert system ready for dashboard integration  
- Frontend-ready responses  
- Scalable architecture  

You can build the entire frontend using this README as your backend reference — without reopening the Django codebase.


- Secure by default  
- User-isolated  
- Frontend-friendly  
- Cleanly structured  
- Easily extensible  

---

# 🎯 Project Objectives

- 🔐 Secure authentication  
- 📦 User-owned product management  
- 📂 Category-based organization  
- ⚠️ Automatic low stock detection  
- ⏳ Expired product alerts  
- 🔒 Strict user-level data isolation  
- 🧱 Clean RESTful architecture  

---

# 🏗️ Architecture Overview

Each user owns:

- Multiple categories  
- Multiple products (inside categories)

### Data relationship

```
User
 └── Category (owner = user)
      └── Product (category → owner)
```

All queries are filtered by:

```python
category__owner=request.user
```

This guarantees no cross-user data access.

---

# 🔐 Authentication

All protected endpoints require authentication.

### Header format (Token)

```
Authorization: Token <your_token>
```

### OR (JWT)

```
Authorization: Bearer <your_access_token>
```

---

# 🌍 Base API URL

```
/api/
```

---

# 👤 AUTHENTICATION ENDPOINTS

## 📝 Register  
**POST** `/api/register/`

### Request
```json
{
  "username": "mohamed",
  "email": "mohamed@email.com",
  "password": "StrongPassword123"
}
```

### Response
```json
{
  "id": 1,
  "username": "mohamed",
  "email": "mohamed@email.com"
}
```

---

## 🔑 Login  
**POST** `/api/login/`

### Request
```json
{
  "username": "mohamed",
  "password": "StrongPassword123"
}
```

### Response
```json
{
  "token": "your_auth_token_here"
}
```

Store token in:

- LocalStorage (simple apps)  
- HTTP-only cookies (recommended for production)  

---

# 📂 CATEGORY ENDPOINTS

Categories belong to the authenticated user.

## 📋 List Categories  
**GET** `/api/categories/`

### Response
```json
[
  {
    "id": 1,
    "name": "Electronics",
    "created_at": "2026-02-10T10:00:00Z"
  }
]
```

## ➕ Create Category  
**POST** `/api/categories/`

```json
{
  "name": "Food"
}
```

## ✏️ Update Category  
**PATCH** `/api/categories/{id}/`

## ❌ Delete Category  
**DELETE** `/api/categories/{id}/`

---

# 📦 PRODUCT ENDPOINTS

Products belong to categories.  
Categories belong to users.  
Products are always user-scoped.

## 📋 List Products  
**GET** `/api/products/`

## 🔍 Retrieve Product  
**GET** `/api/products/{id}/`

## ➕ Create Product  
**POST** `/api/products/`

```json
{
  "name": "Laptop",
  "price": "1200.00",
  "quantity": 10,
  "min_threshold": 3,
  "expiration_date": "2026-12-31",
  "category": 2
}
```

## ✏️ Update Product  
**PATCH** `/api/products/{id}/`

Example:

```json
{
  "quantity": 2
}
```

## ❌ Delete Product  
**DELETE** `/api/products/{id}/`

---

# ⚠️ ALERT SYSTEM

**GET** `/api/products/alerts/`  
Authentication required.

Returns:

- `low_stock`
- `expired`

---

## 🔎 Low Stock Definition

A product is low stock if:

```
quantity <= min_threshold
```

Uses Django `F()` expressions for database-level comparison.

---

## ⏳ Expired Definition

A product is expired if:

```
expiration_date IS NOT NULL
AND expiration_date <= today
```

Date comparison uses timezone-aware server logic.

---

## Example Response

```json
{
  "low_stock": [
    {
      "id": 2,
      "name": "Laptop",
      "price": "1200.00",
      "quantity": 2,
      "min_threshold": 3,
      "expiration_date": null,
      "category": 2,
      "is_low_stock": true,
      "has_expiry": false,
      "created_at": "2026-02-17T11:58:58.098847Z"
    }
  ],
  "expired": [
    {
      "id": 5,
      "name": "Water",
      "price": "2.50",
      "quantity": 10,
      "min_threshold": 2,
      "expiration_date": "2020-01-01",
      "category": 1,
      "is_low_stock": false,
      "has_expiry": true,
      "created_at": "2026-02-10T08:00:00Z"
    }
  ]
}
```

---

📊 DASHBOARD ENDPOINT
📈 Inventory Analytics Overview

GET /api/dashboard/
Authentication required.

Returns a complete inventory summary for the authenticated user.

What It Provides
📦 Counts

Total products

Total categories

Low stock count

Expired products count

📦 Stock

Total stock quantity

💰 Financial Metrics

Total inventory value (price × quantity)

Expired inventory value

Real inventory value (active stock only)

📊 Analytics

Inventory value grouped by category

Example Response
{
  "counts": {
    "total_products": 5,
    "total_categories": 2,
    "low_stock": 2,
    "expired_products": 1
  },
  "stock": {
    "total_stock": 31
  },
  "financial": {
    "total_inventory_value": 36800.0,
    "expired_inventory_value": 5000.0,
    "real_inventory_value": 31800.0
  },
  "analytics": {
    "value_by_category": [
      {
        "category": "Electronics",
        "total_value": 29000.0
      },
      {
        "category": "Fruits",
        "total_value": 7800.0
      }
    ]
  }
}



# 🧠 Product Object Reference

| Field | Type | Description |
|-------|------|------------|
| id | Integer | Primary key |
| name | String | Product name |
| price | Decimal | Product price |
| quantity | Integer | Current stock |
| min_threshold | Integer | Alert threshold |
| expiration_date | Date (nullable) | Expiry date |
| category | Integer | Category ID |
| created_at | DateTime | Creation timestamp |
| is_low_stock | Boolean | Computed field |
| has_expiry | Boolean | True if expiration_date exists |

---

# 🔒 Security Model

- All endpoints (except register/login) require authentication  
- Products filtered by category ownership  
- Categories filtered by owner  
- No direct product-user relation exposed  
- Backend enforces ownership rules  

---

# 🖥️ Frontend Integration Reference

## Typical Dashboard Flow

1. Login → store token  
2. Fetch categories  
3. Fetch products  
4. Fetch alerts  
5. Render dashboard widgets  

## Suggested Dashboard Widgets

- Total Products  
- Total Categories  
- Low Stock Count  
- Expired Products Count  

Use:

```
GET /api/products/alerts/
```

to populate notification badges.

---

# 🧪 How to Trigger Alerts (Testing)

## Trigger Low Stock

```json
{
  "quantity": 2,
  "min_threshold": 3
}
```

## Trigger Expired

```json
{
  "expiration_date": "2020-01-01"
}
```

---

# 📦 Installation (Backend)

```bash
git clone <repository-url>
cd Gestion-de-Stock-Intelligent-django

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
```

---

# 🛠️ Possible Future Enhancements

- Pagination  
- Search & filtering  
- Sales tracking  
- Stock movement history  
- Email alerts  
- Admin dashboard  
- Role-based permissions  
- Docker deployment  
- CI/CD pipeline  

---

# 🏁 Conclusion

This API provides:

- Clean REST structure  
- Secure user isolation  
- Alert system ready for dashboard integration  
- Frontend-ready responses  
- Scalable architecture  

