# MoneyMesh - Finance Data Processing and Access Control Backend

## Overview

MoneyMesh is a backend system designed for managing personal or organizational financial data with secure role-based access.

This project is a backend system for managing financial records with role-based access control and dashboard analytics. It is designed to simulate a real-world finance dashboard where different users interact with data based on their roles.

The system focuses on clean architecture, proper data handling, secure access control, and meaningful aggregation of financial data.

---

## Tech Stack

* **Backend Framework:** FastAPI
* **Database:** SQLite
* **ORM:** SQLAlchemy
* **Authentication:** JWT (JSON Web Tokens)
* **Validation:** Pydantic

---

## Key Features

### 1. User and Role Management

* Create and manage users
* Assign roles: `admin`, `analyst`, `viewer`
* Activate/deactivate users
* Enforce role-based permissions

### Role Permissions

* **Admin**

  * Full access to users and financial records
  * Can create, update, delete records and manage users

* **Analyst**

  * Can view financial records
  * Can access dashboard analytics

* **Viewer**

  * Can only view data and dashboard summaries

---

### 2. Authentication and Authorization

* JWT-based authentication
* Secure password hashing using bcrypt
* Token-based user identification
* Role-based access control using FastAPI dependencies

---

### 3. Financial Records Management

* Create, read, update, and delete financial records
* Each record includes:

  * Amount
  * Type (income/expense)
  * Category
  * Date
  * Notes
* User-specific data isolation (records belong to a user)

---

### 4. Filtering and Querying

* Filter records by:

  * Type
  * Category
  * Date range
* Combined filtering supported
* Sorted results (latest first)

**Example:**

```
GET /records?type=expense&category=food&start_date=2026-04-01&end_date=2026-04-30
```

---

### 5. Dashboard APIs

* Total income
* Total expenses
* Net balance
* Category-wise aggregation
* Recent activity
* Monthly trends

---

### 6. Validation and Error Handling

* Input validation using Pydantic
* Proper HTTP status codes
* Duplicate record prevention
* Ownership checks for secure updates/deletes

---

### 7. Data Persistence

* SQLite database for simplicity and quick setup
* Structured relational schema using SQLAlchemy

---

## Project Structure

```
app/
├── core/            # Security, dependencies, roles
├── db/              # Database setup and session
├── models/          # SQLAlchemy models
├── schemas/         # Pydantic schemas
├── routes/          # API endpoints
├── services/        # Business logic
└── main.py          # Entry point
```

---

## Setup Instructions

### 1. Clone the repository

```
git clone https://github.com/Mitali-A13/MoneyMesh.git
cd MoneyMesh
```

### 2. Create virtual environment

```
uv venv
source .venv/bin/activate
```

### 3. Install dependencies

```
uv pip install fastapi uvicorn sqlalchemy pydantic python-jose passlib[bcrypt]
```

### 4. Run the server

```
uvicorn app.main:app --reload
```

### 5. Access API Docs

```
http://127.0.0.1:8000/docs
```

---

## API Overview

### Authentication

* `POST /auth/register` – Register user
* `POST /auth/login` – Authenticate user and retrieve JWT token

### Users

* `GET /users` – Retrieve all users (accessible based on role permissions)
* `PUT /users/{user_id}` – Update user details (admin only)
* `PATCH /users/{user_id}/toggle-status` – Toggle user active/inactive status (admin only)

### Financial Records

* `POST /records` – Create record (admin only)
* `GET /records` – Get records (with filters)
* `PUT /records/{record_id}` – Update record
* `DELETE /records/{record_id}` – Delete record

### Dashboard

* `GET /dashboard/summary`
* `GET /dashboard/categories`
* `GET /dashboard/recent`
* `GET /dashboard/trends`

---

## Authentication Usage

Include the JWT token in headers:

```
Authorization: Bearer <your-token>
```

---

## How to Test the API

1. Register a user using `/auth/register`
2. Login using `/auth/login` to receive a JWT token
3. Click "Authorize" in Swagger UI and provide the token:

   ```
   Bearer <your-token>
   ```
4. Access protected endpoints such as `/records` or `/dashboard`

---

## Key Design Decisions

### 1. Use of FastAPI

FastAPI was chosen for its performance, simplicity, and built-in dependency injection system, which enables clean implementation of middleware-like logic such as authentication and role-based access.

### 2. Layered Architecture

The application is divided into:

* Routes (API layer)
* Services (business logic)
* Models (database)
* Schemas (validation)

This ensures separation of concerns and maintainability.

The system follows a service-oriented architecture where business logic is isolated from API routes, improving scalability and testability.

### 3. JWT-Based Authentication

JWT was implemented to:

* Simulate real-world authentication
* Enable stateless user sessions
* Ensure secure user identification across requests

### 4. Role-Based Access Control (RBAC)

Access control is enforced using dependency injection, allowing reusable and centralized permission checks.

### 5. User-Specific Data Isolation

All financial data is scoped to the authenticated user, ensuring that users can only access their own records.

### 6. SQLite for Development

SQLite was chosen for simplicity and quick setup, while still maintaining relational integrity.

---

## Trade-offs

* SQLite used instead of production-grade database for ease of setup
* JWT implementation is minimal (no refresh tokens)
* No caching or rate limiting included
* No pagination implemented to keep scope focused

---

## Future Improvements

* Add pagination for large datasets
* Implement refresh tokens for authentication
* Add soft delete functionality
* Introduce rate limiting
* Add unit and integration tests
* Migrate to PostgreSQL for production

---

## Conclusion

This project demonstrates backend design principles including structured architecture, role-based access control, secure authentication, and efficient data processing. The focus was on building a clean, maintainable, and logically sound system aligned with real-world backend practices.
