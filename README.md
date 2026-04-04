# 💰 Finance Dashboard API

A robust backend REST API for managing financial records and generating dashboard analytics. Built with **Django 6.0+** and **Django REST Framework**, this application features Role-Based Access Control (RBAC), JWT authentication, soft-deletion for records, CSV exports, and advanced aggregated analytics.

---

## 🚀 Features

* **JWT Authentication:** Secure stateless authentication using `djangorestframework-simplejwt`.
* **Role-Based Access Control (RBAC):** Three distinct user roles (`ADMIN`, `ANALYST`, `VIEWER`) with custom permission classes.
* **Comprehensive Finance Management:** Track income and expenses. Supports soft-delete, restore, and hard-delete operations (Admin only).
* **Dashboard & Analytics:** Powerful data aggregation providing total summaries, monthly/weekly trends, category breakdowns, and recent activities.
* **Data Export:** Download filtered financial records as CSV files.
* **API Rate Limiting:** Built-in throttling to prevent abuse (e.g., Viewers limited to 10 requests/minute).
* **Interactive API Documentation:** Auto-generated OpenAPI/Swagger UI via `drf-spectacular`.

---

## 🛠️ Tech Stack

* **Python:** 3.13+
* **Frameworks:** Django 6.0.3, Django REST Framework 3.17
* **Authentication:** PyJWT, SimpleJWT
* **Documentation:** drf-spectacular (OpenAPI 3)
* **Package Management:** `uv` (lockfile provided) or standard `pip`

---

## 👥 User Roles

1. **Admin (`ADMIN`)**

   * Full access to the system
   * Manage users
   * Create/edit/delete/restore financial records
   * Export CSVs
   * View dashboards

2. **Analyst (`ANALYST`)**

   * Read-only access to detailed financial records
   * Access to dashboard analytics

3. **Viewer (`VIEWER`)**

   * Basic read-only access (e.g., dashboards)
   * Strict rate limiting (10 requests/min)

---

## ⚙️ Prerequisites

* Python 3.13 or higher
* [uv](https://github.com/astral-sh/uv) *(Recommended)* or `pip`

---

## 💻 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Krish-4801/Finance-Dashboard.git
cd Finance-Dashboard
```

---

### 2. Set Up Virtual Environment & Install Dependencies

#### Using `uv` (Recommended)

```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip sync uv.lock
```

#### Using `pip`

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

---

### 3. Configure Environment Variables

Create a `.env` file in your backend directory:

```ini
SECRET_KEY=your-super-secret-django-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

---

### 4. Run Migrations

```bash
cd backend
python manage.py migrate
```

---

### 5. Create Superuser (Initial Admin)

```bash
python manage.py createsuperuser
```

---

### 6. Start Development Server

```bash
python manage.py runserver
```

---

## 📚 API Documentation

Once the server is running:

* **Swagger UI:** http://127.0.0.1:8000/api/docs/
* **OpenAPI Schema:** http://127.0.0.1:8000/api/schema/

---

## 🛣️ Main API Endpoints

### 🔐 Authentication (`/api/users/`)

* `POST /api/users/login/` → Obtain JWT Access & Refresh tokens
* `POST /api/users/refresh/` → Refresh access token

---

### 👤 User Management (`/api/users/manage/`) *(Admin Only)*

* `GET /api/users/manage/` → List all users
* `POST /api/users/manage/` → Create new user with role
* `POST /api/users/manage/{id}/toggle_active/` → Activate/Deactivate user

---

### 💳 Finance Records (`/api/finance/`)

* `GET /api/finance/records/` → List records *(supports filtering, search, ordering)*
* `POST /api/finance/records/` → Add record
* `DELETE /api/finance/records/{id}/` → Soft delete
* `POST /api/finance/records/{id}/restore/` → Restore *(Admin only)*
* `DELETE /api/finance/records/{id}/hard_del/` → Permanent delete *(Admin only)*
* `GET /api/finance/downloads/` → Export records as CSV
### 📥 Download Records (CSV Export)

* `GET /api/finance/downloads/`

Provides:

* Exported CSV of filtered financial records

Supports query params:

* `start_date` (YYYY-MM-DD)
* `end_date` (YYYY-MM-DD)
* `category`
* `type` (income/expense)

---



---

### 📊 Dashboard Analytics (`/api/dashboard/`)

* `GET /api/dashboard/summary/`

Provides:

* Net balance
* Weekly & monthly trends
* Category breakdown
* Recent transactions

Supports query params:

* `start_date`
* `end_date`
* `recents`

---

## ✅ Summary

This API provides a **secure, scalable, and production-ready backend** for financial tracking applications, with:

* Fine-grained access control (RBAC)
* Real-time analytics
* Clean RESTful design
* Extensible architecture

Perfect for dashboards, fintech tools, and internal financial systems.

---
