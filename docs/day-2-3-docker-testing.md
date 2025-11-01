# Day 2-3: Docker Compose & Testing Infrastructure

**Date:** October 28, 2025  
**Technologies:** Docker, Docker Compose, PostgreSQL, pytest, httpx

---

## What We Built

### 1. Docker Compose Setup
Created multi-container orchestration for local development.

**File: `docker-compose.yml`**
```yaml
services:
  postgres:
    image: postgres:15-alpine
    ports: ["5432:5432"]
    healthcheck: pg_isready
  
  backend:
    build: ./backend
    ports: ["8080:8080"]
    depends_on:
      postgres: service_healthy
```

**Key Concepts:**
- **Multi-container orchestration**: Run database + backend together
- **Health checks**: Backend waits for database to be ready
- **Volume persistence**: Database data survives container restarts
- **Service dependencies**: Automatic startup order

**Why This Matters:**
- Matches production environment locally
- Easy onboarding for new developers (`docker-compose up`)
- Consistent environment across team
- Industry standard for local development

### 2. Simplified Dockerfile
Updated backend Dockerfile for docker-compose compatibility.

**Before vs After:**
```dockerfile
# Before: Complex multi-stage with frontend
COPY website/dist/ ../website/dist/
RUN python init_db.py && python migrate_data.py

# After: Simple, focused on backend
COPY . .
CMD ["python", "run.py"]
```

**Why:**
- Separation of concerns (frontend separate)
- Faster builds (no frontend compilation)
- Easier to debug
- Better layer caching

### 3. .dockerignore
Created `.dockerignore` to keep Docker images small.

**What it excludes:**
- `__pycache__/` - Python bytecode cache
- `*.pyc` - Compiled Python files
- `.env` - Environment secrets
- `*.db` - Local database files
- `.pytest_cache` - Test cache

**Impact:**
- Smaller images (50-100MB saved)
- Faster builds (less to copy)
- No accidental secrets in images
- Professional setup

### 4. Testing Infrastructure (pytest)
Set up complete testing framework with fixtures and async support.

**Files Created:**
```
backend/tests/
├── __init__.py
├── conftest.py       # Shared fixtures
├── test_main.py      # Basic API tests
├── test_wines.py     # Wine endpoint tests
└── test_auth.py      # Authentication tests
```

**Test Coverage:**
- Health check endpoint
- Wine filtering (color, availability)
- Authentication flows
- Protected endpoints

**Running tests:**
```bash
cd backend
pytest tests/ -v
```

### 5. pytest Configuration
Created `pyproject.toml` with pytest settings.

**Configuration:**
```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
addopts = "-v --strict-markers"
```

**Features:**
- Automatic async test detection
- Verbose output by default
- Strict marker enforcement
- Test discovery patterns

---

## Interview Talking Points

### Question: "How do you set up local development environments?"

**Answer:**
"I use Docker Compose to orchestrate all services locally. For this project:
- PostgreSQL database in one container
- FastAPI backend in another
- Volumes for data persistence
- Health checks ensure proper startup order

A new developer can run `docker-compose up` and have the entire stack running in minutes. This matches our production environment and eliminates 'works on my machine' issues."

### Question: "What's your testing strategy?"

**Answer:**
"I use pytest with async support for testing FastAPI endpoints:
- **Unit tests**: Individual endpoint behavior
- **Integration tests**: Database interactions
- **Test fixtures**: Reusable database sessions
- **Async testing**: Tests actual async behavior

Currently at 10+ tests covering health checks, authentication, and CRUD operations. Tests run automatically in CI/CD before deployment."

### Question: "Why Docker for local development?"

**Answer:**
"Docker provides several benefits:
1. **Consistency** - Same environment everywhere
2. **Isolation** - No conflicts with system Python
3. **Easy setup** - One command to start everything
4. **Production parity** - Local matches cloud deployment
5. **Team collaboration** - Everyone has identical setup"

### Question: "How do you handle test databases?"

**Answer:**
"I use SQLite for test isolation:
```python
# conftest.py
TEST_DATABASE_URL = 'sqlite:///./test.db'

@pytest.fixture
def db_session():
    Base.metadata.create_all(engine)
    db = TestingSessionLocal()
    yield db
    Base.metadata.drop_all(engine)
```

Each test gets a fresh database, ensuring tests don't interfere with each other. For integration tests, we can use PostgreSQL in Docker with the same pattern."

---

## Code Snippets to Remember

### Docker Compose Service Definition
```yaml
services:
  backend:
    build:
      context: .
      dockerfile: backend/Dockerfile
    environment:
      DATABASE_URL: postgresql://user:pass@postgres:5432/db
    depends_on:
      postgres:
        condition: service_healthy
```

### FastAPI Test Pattern
```python
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_endpoint():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.get("/api/wines/")
    
    assert response.status_code == 200
    assert isinstance(response.json(), list)
```

### Test Fixture for Database
```python
@pytest.fixture
async def async_db_session():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with AsyncSessionLocal() as session:
        yield session
    
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
```

---

## Technologies Deep Dive

### Docker Compose
- **What**: Tool for defining multi-container Docker applications
- **Why**: Simplifies complex setups, manages networking, volumes
- **Use**: Local development, testing, small deployments

### pytest-asyncio
- **What**: pytest plugin for testing async code
- **Why**: FastAPI is async, need proper async testing
- **Use**: `@pytest.mark.asyncio` decorator for async tests

### httpx
- **What**: HTTP client with async support
- **Why**: FastAPI's `TestClient` uses it, supports async requests
- **Use**: Testing API endpoints without running server

### Health Checks in Docker
```yaml
healthcheck:
  test: ["CMD-SHELL", "pg_isready -U user"]
  interval: 10s
  timeout: 5s
  retries: 5
```
- Ensures database is ready before backend starts
- Prevents connection errors on startup
- Industry best practice

---

## Common Mistakes Avoided

1. **No .dockerignore** → Large images with cache files
2. **No health checks** → Backend starts before database ready
3. **Hardcoded test URLs** → Used `http://test` with ASGITransport
4. **Sync test client for async app** → Used AsyncClient properly
5. **Shared test database** → Each test gets fresh DB

---

## What's Next (Day 4 Preview)

- Mobile admin panel enhancements
- Bulk operations API
- Better responsive design
- Touch-friendly buttons (44px+ tap targets)

---

## Quick Reference

**Start services:**
```bash
docker-compose up -d
```

**Run tests:**
```bash
cd backend
pytest tests/ -v
```

**Check logs:**
```bash
docker-compose logs -f backend
```

**Stop services:**
```bash
docker-compose down
```

**Rebuild after changes:**
```bash
docker-compose up --build
```

---

## Metrics

**Tests Added:** 10 tests across 3 files
**Test Coverage:** Health, wines, auth endpoints
**Docker Images:** 2 services (postgres, backend)
**Lines of Code:** ~150 (tests + config)
**Build Time:** ~30 seconds
**Test Runtime:** <1 second
