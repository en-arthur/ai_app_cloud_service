# AI App CloudService

**Backend API service** for AI-generated apps — provides authentication, storage, and file management out of the box.

## How It Works

```
WorkersCraft Platform
  └─ User generates an app with backend enabled
  └─ Calls /api/apps/register → gets app_id
  └─ Injects SDK with app_id into the generated app code

CloudService (this repo)
  └─ Multi-tenant REST API
  └─ Each app is isolated by app_id
  └─ Each user's data is isolated within their app

Generated App (running in browser)
  └─ Uses injected SDK to call CloudService
  └─ Auth, storage, file uploads — all handled
```

## Features

- 🔐 JWT auth with refresh tokens (register, login, logout)
- 💾 Generic JSONB storage (store any data structure)
- 📁 File upload/download via Cloudflare R2
- 🏢 Multi-tenant isolation per app
- 👤 User-level data isolation

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
```

Fill in `.env`:

| Variable | Description |
|---|---|
| `DATABASE_URL` | PostgreSQL connection string |
| `JWT_SECRET` | Random secret key for signing tokens |
| `R2_ENDPOINT` | Cloudflare R2 endpoint URL |
| `R2_ACCESS_KEY_ID` | R2 access key |
| `R2_SECRET_ACCESS_KEY` | R2 secret key |
| `R2_BUCKET_NAME` | R2 bucket name |
| `R2_PUBLIC_URL` | Public URL for serving files |
| `CORS_ORIGINS` | Comma-separated allowed origins (use `*` for dev) |

### 3. Set up the database

```bash
# Create the database
createdb cloudservice

# Run migrations
alembic upgrade head
```

### 4. Run the server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- API: http://localhost:8000
- Interactive docs: http://localhost:8000/docs

---

## API Reference

### Apps
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/apps/register` | Register a new app (called by WorkersCraft) |
| GET | `/api/apps/{app_id}` | Get app details |
| GET | `/api/apps/owner/{owner_id}` | List all apps for an owner |
| DELETE | `/api/apps/{app_id}` | Deactivate an app |

### Auth (per app)
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/register` | Register a user in an app |
| POST | `/api/auth/login` | Login and get tokens |
| POST | `/api/auth/refresh` | Refresh access token |
| POST | `/api/auth/logout` | Logout (revoke refresh token) |
| GET | `/api/auth/me` | Get current user |

### Storage (per app, per user)
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/storage/{collection}` | Create a record |
| GET | `/api/storage/{collection}` | List records |
| GET | `/api/storage/{collection}/{id}` | Get a record |
| PUT | `/api/storage/{collection}/{id}` | Update a record |
| DELETE | `/api/storage/{collection}/{id}` | Delete a record |

### Files (per app, per user)
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/files/upload` | Upload a file to R2 |
| GET | `/api/files` | List files |
| DELETE | `/api/files/{file_id}` | Delete a file |

---

## Development

### Create a migration

```bash
alembic revision --autogenerate -m "your description"
```

### Apply migrations

```bash
alembic upgrade head
```

### Rollback

```bash
alembic downgrade -1
```

## Project Structure

```
app/
├── main.py           # FastAPI app + CORS
├── config.py         # Settings from .env
├── database.py       # DB session
├── models/           # SQLAlchemy models
├── routers/          # Route handlers
├── services/         # Business logic
├── schemas/          # Pydantic schemas
├── middleware/       # JWT auth middleware
└── utils/            # JWT helpers, errors, password hashing
alembic/              # DB migrations
```
