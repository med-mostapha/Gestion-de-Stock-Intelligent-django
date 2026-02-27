# 📦 Gestion de Stock Intelligent API
**Stock Management • Alert System • Inventory Analytics • Secure REST Architecture**

A production-ready Django REST API for inventory management with analytics dashboard, filtering, pagination, and strict user-level isolation.

---

# 🚀 Tech Stack

- Python 3
- Django 6
- Django REST Framework
- PostgreSQL
- Token Authentication
- Django Filter
- Gunicorn (production)
- dj-database-url
- CORS Headers

---

# 🏗️ Architecture Overview

### Custom User Model
- Extends `AbstractUser`
- Adds optional `phone` field
- Token-based authentication

### Data Ownership Model

```
User
 └── Category (owner = user)
      └── Product (category → owner)
```

All product queries are filtered by:

```python
category__owner=request.user
```

This guarantees strict multi-tenant isolation.

---

# 🔐 Authentication

Token-based authentication.

### Header Format

```
Authorization: Token <your_token>
```

### Auth Endpoints

#### 📝 Register
`POST /api/register/`

```json
{
  "username": "mohamed",
  "email": "user@email.com",
  "password": "StrongPassword123",
  "phone": "12345678"
}
```

#### 🔑 Login
`POST /api/login/`

```json
{
  "username": "mohamed",
  "password": "StrongPassword123"
}
```

Response:

```json
{
  "token": "your_auth_token"
}
```

---

# 📂 Category Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/categories/` | List user categories |
| POST | `/api/categories/` | Create category |
| GET | `/api/categories/{id}/` | Retrieve |
| PATCH | `/api/categories/{id}/` | Update |
| DELETE | `/api/categories/{id}/` | Delete |

Categories are automatically assigned to authenticated user.

---

# 📦 Product Endpoints

### Features Included
- Pagination
- Filtering by category
- Search by name
- Ordering by price, quantity, created_at
- Annotated fields: `is_low_stock`, `has_expiry`

| Method | Endpoint |
|--------|----------|
| GET | `/api/products/` |
| POST | `/api/products/` |
| GET | `/api/products/{id}/` |
| PATCH | `/api/products/{id}/` |
| DELETE | `/api/products/{id}/` |

### Example Create

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

---

# ⚠️ Alert Endpoint

`GET /api/products/alerts/`

Returns:

- `low_stock`
- `expired`

### Low Stock Logic

```
quantity <= min_threshold
```

### Expired Logic

```
expiration_date <= today
```

---

# 📊 Dashboard Endpoint

## `GET /api/dashboard/`

Returns a full inventory analytics summary.

### 📦 Counts
- Total products
- Total categories
- Low stock count
- Expired products count

### 📦 Stock
- Total stock quantity

### 💰 Financial Metrics
- Total inventory value
- Expired inventory value
- Real inventory value (active stock only)

### 📊 Category Analytics
- Inventory value grouped by category

---

### Example Response

```json
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
  "analytics": [
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
```

---

# 🧠 Product Model Reference

| Field | Type |
|-------|------|
| id | Integer |
| name | String |
| price | Decimal |
| quantity | Integer |
| min_threshold | Integer |
| expiration_date | Date (nullable) |
| category | FK |
| created_at | DateTime |
| is_low_stock | Boolean (annotated) |
| has_expiry | Boolean (annotated) |

---

# 🔎 Filtering, Search & Ordering

Supported on product list:

```
/api/products/?category=2
/api/products/?search=laptop
/api/products/?ordering=price
/api/products/?ordering=-created_at
```

---

# 📄 Pagination

Default page size: 10  
Custom page size:

```
/api/products/?page_size=20
```

Max page size: 100

---

# ⚙️ Environment Configuration

Create `.env` file:

```
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=postgres://user:password@localhost:5432/dbname
ALLOWED_HOSTS=127.0.0.1,localhost
```

---

# 🛠 Installation

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

# 🏭 Production Notes

Currently:

- Token authentication enabled
- PostgreSQL required
- Gunicorn included
- CORS enabled globally (dev mode)

⚠️ For production:
- Restrict `ALLOWED_HOSTS`
- Disable `DEBUG`
- Restrict CORS
- Enable SSL
- Add rate limiting
- Add caching
- Add tests

---

# 🧱 Project Strengths

- Clean multi-tenant architecture
- Secure ownership validation in serializer
- Aggregation-based dashboard (DB-level calculations)
- Search + filtering + ordering
- Pagination
- Custom user model
- Production-ready database configuration

---

# 📈 Future Improvements

- JWT support
- Swagger / OpenAPI documentation
- Docker setup
- Unit & integration tests
- Role-based permissions
- Rate limiting
- Caching dashboard
- CI/CD pipeline

---

# 🏁 Summary

This API delivers:

- Secure user-isolated inventory management
- Real-time low stock & expiration alerts
- Financial analytics dashboard
- RESTful scalable architecture
- Frontend-ready responses

Suitable for:
- SaaS inventory system
- Admin dashboard backend
- Mobile app backend
- Portfolio-level backend project
