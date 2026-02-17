# 📦 Gestion de Stock Intelligent API

### Stock Management • Alert System • Secure REST Architecture

This project is a secure and scalable **Django REST API** built to manage inventory with an intelligent alert system. It handles everything from user isolation to stock thresholds and expiration monitoring.

---

## 🚀 Overview
Designed to be frontend-friendly (for Expo/React Native) and backend-secure, this API ensures:
* **Secure by default:** JWT/Token based authentication.
* **User-isolated:** Every user has their own private space.
* **Intelligent Alerts:** Automated detection of low stock and expired goods.
* **Cleanly Structured:** Follows RESTful best practices.

---

## 🎯 Project Objectives
- 🔐 **Secure authentication** (Register/Login).
- 📦 **User-owned management:** Full CRUD for Categories and Products.
- 📂 **Category-based organization.**
- ⚠️ **Automatic low stock detection** based on custom thresholds.
- ⏳ **Expired product alerts.**
- 🔒 **Strict data isolation:** Users can never see each other's data.

---

## 🏗️ Architecture Overview
The system follows a hierarchical ownership model:

**User** └── **Category** (owner = user)  
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── **Product** (linked to category)

> **Isolation Logic:** All database queries are filtered by `category__owner=request.user`. This guarantees that even if a user guesses a Product ID, they cannot access it unless they own the parent category.

---

## 🔐 Authentication
Protected endpoints require an Authorization header.

**Header Format:**
```http
Authorization: Token <your_auth_token>
