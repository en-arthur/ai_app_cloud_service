# WorkersCraft CloudService

**Backend API service** for generated apps with authentication, storage, and file management.

## Architecture

```
WorkersCraft Platform (generates apps)
  └─ Generates frontend code with SDK
  └─ Calls CloudService to register app
  └─ Injects SDK with app_id into generated code

CloudService (this repo - backend API)
  └─ Provides REST API for all generated apps
  └─ Handles auth, storage, files
  └─ Multi-tenant isolation

Generated Apps (user's apps)
  └─ Include SDK (from WorkersCraft)
  └─ Call CloudService API for backend features
```

**Note:** The SDK template lives in WorkersCraft, not here. CloudService only provides the API endpoints.

## Features

- 🔐 JWT Authentication with refresh tokens
- 💾 Generic JSONB storage (any data structure)
- 📁 File upload to Cloudflare R2
- 🏢 Multi-tenant isolation (app-level)
- 👤 User-level data isolation

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your database and R2 credentials
```

### 3. Setup Database

```bash
# Create PostgreSQL database
createdb cloudservice

# Run migrations
alembic upgrade head
```

### 4. Run Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Server will be available at: http://localhost:8000

API docs: http://localhost:8000/docs

## API Endpoints

### App Registration

```bash
POST /api/apps/register
Body: { "project_id": "uuid", "name": "My App", "owner_id": "uuid" }
Returns: { "app_id": "uuid" }
```

### Health Check

```bash
GET /health
Returns: { "status": "healthy" }
```

## Development

### Create Migration

```bash
alembic revision --autogenerate -m "description"
```

### Apply Migrations

```bash
alembic upgrade head
```

### Rollback Migration

```bash
alembic downgrade -1
```

## Project Structure

```
app/
├── main.py              # FastAPI app
├── config.py            # Configuration
├── database.py          # Database connection
├── models/              # SQLAlchemy models
├── routers/             # API routes
├── services/            # Business logic
├── middleware/          # Auth middleware
├── schemas/             # Pydantic schemas
└── utils/               # Utilities
```

## Next Steps

- [ ] Phase 3: Authentication with JWT
- [ ] Phase 4: Storage API (CRUD)
- [ ] Phase 5: File Upload (R2)
- [ ] Phase 6: SDK Generation
- [ ] Phase 7: WorkersCraft Integration
