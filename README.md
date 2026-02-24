# 📦 Gestion de Stock Intelligent API

**Stock Management • Alert System • Secure REST Architecture**

A high-performance, secure, and scalable Django 6.0 REST API designed for intelligent inventory tracking, financial analytics, and automated stock alerts.

---

## 🚀 Key Features

- 🔐 **Secure Authentication**: Token-based authentication with strict user-level data isolation.
- 📊 **Advanced Dashboard**: Real-time financial analytics and stock counts calculated directly in PostgreSQL for maximum speed.
- ⚠️ **Smart Alert System**: Automatic detection of low stock ($quantity \le threshold$) and expired products.
- 🔍 **Pro Search & Filtering**: Built-in search by name, filtering by category, and multi-field sorting.
- 📑 **Optimized Pagination**: Standardized Page-Number pagination for handling large datasets.
- 📥 **Reporting**: One-click CSV export functionality for inventory audits.
- 🐘 **Production Ready**: Fully integrated with PostgreSQL and environment-based configuration.

---

## 🏗️ Architecture Overview

The system follows a strict ownership model to ensure data privacy:

- **User**: The root owner.
- **Category**: Belongs to a User.
- **Product**: Linked to a Category (Inherits ownership from Category).

> **Note:** All queries are filtered at the database level using `category__owner=request.user`.

---

## 🔑 Authentication Endpoints

| Action       | Method | URL              | Authentication |
| :----------- | :----- | :--------------- | :------------- |
| **Register** | POST   | `/api/register/` | None           |
| **Login**    | POST   | `/api/login/`    | None           |

**Header Format:** All protected requests must include: `Authorization: Token <your_token>`

---

## 📂 Inventory Endpoints

### Categories

- **List/Create**: `GET/POST` `/api/categories/`
- **Detail/Update/Delete**: `GET/PUT/PATCH/DELETE` `/api/categories/{id}/`

### Products

- **List/Create**: `GET/POST` `/api/products/`
- **Detail/Update/Delete**: `GET/PUT/PATCH/DELETE` `/api/products/{id}/`

---

## 🔍 Search, Filter & Sorting

The `/api/products/` endpoint supports powerful query parameters:

| Feature     | Query Parameter | Example                          |
| :---------- | :-------------- | :------------------------------- |
| **Search**  | `?search=`      | `/api/products/?search=laptop`   |
| **Filter**  | `?category=`    | `/api/products/?category=2`      |
| **Sorting** | `?ordering=`    | `/api/products/?ordering=-price` |

---

## ⚠️ Intelligence & Analytics

### 📊 Dashboard

**GET** `/api/dashboard/`  
Returns total inventory value, expired stock value, and category-wise financial distribution.

### 🔔 Alerts

**GET** `/api/products/alerts/`  
Returns two specific lists:

1. `low_stock`: Products where $quantity \le min\_threshold$.
2. `expired`: Products where $expiration\_date \le today$.

### 📥 Export

**GET** `/api/products/export/`  
Generates and downloads a `.csv` file of the current user's inventory.

---

## 🛠️ Installation & Setup

### 1. Environment Setup

```bash
git clone <repository-url>
cd Gestion-de-Stock-Intelligent-django
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```
