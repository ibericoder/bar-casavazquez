# Day 1: Environment Configuration & Database Setup

**Date:** October 27, 2025  
**Technologies:** Python, FastAPI, SQLAlchemy, PostgreSQL, Environment Variables

---

## What We Built Today

### 1. Environment Configuration (`.env.example`)
Created a template for environment variables to separate configuration from code.

**Key Concepts:**
- **Environment Variables**: Configuration values stored outside the codebase
- **`.env` files**: Local configuration (never committed to git)
- **`.env.example`**: Template showing what variables are needed (safe to commit)

**Why This Matters:**
- Security: Keeps secrets (API keys, passwords) out of version control
- Flexibility: Different settings for dev/staging/production
- Best Practice: Standard in professional applications

### 2. PostgreSQL Preparation
Enhanced database configuration to support PostgreSQL (production database).

**SQLite vs PostgreSQL:**

| Feature | SQLite | PostgreSQL |
|---------|--------|------------|
| Type | File-based | Server-based |
| Use Case | Development, small apps | Production, scalable apps |
| Concurrency | Limited | Excellent |
| Features | Basic | Advanced (triggers, views, stored procedures) |
| Deployment | Single file | Dedicated server/container |

**Code Changes:**
```python
# Before
if self.database_url.startswith("postgresql://"):
    return self.database_url.replace("postgresql://", "postgresql+asyncpg://")

# After - Added support for Heroku/Railway URLs
if self.database_url.startswith("postgres://"):
    return self.database_url.replace("postgres://", "postgresql+asyncpg://")
```

**Why:** Cloud platforms like Heroku use `postgres://` instead of `postgresql://`

### 3. Connection Pooling
Added `pool_pre_ping=True` to database engines.

**What is Connection Pooling?**
- Reuses database connections instead of creating new ones
- Significantly improves performance
- `pool_pre_ping`: Tests connection before using (handles stale connections)

**Code:**
```python
engine = create_engine(
    settings.database_url,
    connect_args=connect_args,
    pool_pre_ping=True  # Health check before each use
)
```

**Performance Impact:**
- Without pooling: 100-500ms per connection
- With pooling: 1-5ms (reused connection)

### 4. Async Database Support
Configured async database engine for FastAPI's async endpoints.

**Sync vs Async:**
```python
# Sync - Blocks thread while waiting
def get_wines():
    result = db.query(Wine).all()  # Waits here
    return result

# Async - Can handle other requests while waiting
async def get_wines():
    result = await db.execute(select(Wine))  # Doesn't block
    return result
```

**Why Async Matters:**
- Handle 1000s of concurrent requests
- Better resource utilization
- Required for modern web applications

---

## Interview Talking Points

### Question: "Why did you choose FastAPI over Flask or Django?"

**Answer:**
"I chose FastAPI for several reasons:
1. **Native async support** - Better performance for I/O operations like database queries
2. **Automatic API documentation** - Swagger UI out of the box
3. **Type safety with Pydantic** - Catches errors before runtime
4. **Modern Python features** - Uses Python 3.6+ type hints
5. **Performance** - One of the fastest Python frameworks (comparable to Node.js)"

### Question: "How do you handle different environments (dev/staging/prod)?"

**Answer:**
"I use environment variables with `.env` files:
- `.env.example` - Template committed to git
- `.env` - Local configuration (gitignored)
- Production uses environment variables set on the platform

This allows:
- Different database URLs per environment
- Separate API keys for dev/prod
- Debug mode only in development
- Easy deployment without code changes"

### Question: "Explain your database architecture."

**Answer:**
"I use SQLAlchemy ORM with both sync and async engines:
- **Development**: SQLite for quick iteration
- **Production**: PostgreSQL for scalability and features
- **Connection pooling** with health checks (`pool_pre_ping`)
- **Async support** for non-blocking database operations

The async_database_url property automatically converts URLs to the correct format for asyncpg (PostgreSQL) or aiosqlite (SQLite)."

### Question: "What security considerations did you implement?"

**Answer:**
"Several security measures:
1. **Environment variables** - Secrets never in code
2. **`.gitignore`** - Ensures `.env` never committed
3. **Connection pooling** - Prevents connection exhaustion attacks
4. **Database URL validation** - Proper format checking
5. Later added **JWT authentication** for protected endpoints"

---

## Code Snippets to Remember

### Environment Setup Pattern
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "sqlite:///./default.db"
    secret_key: str
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
```

### Database Connection with Pooling
```python
from sqlalchemy import create_engine

connect_args = {}
if "sqlite" in database_url:
    connect_args = {"check_same_thread": False}

engine = create_engine(
    database_url,
    connect_args=connect_args,
    pool_pre_ping=True  # Critical for production
)
```

### Async Database Session
```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

async_engine = create_async_engine(
    async_database_url,
    pool_pre_ping=True
)

async def get_async_db():
    async with AsyncSessionLocal() as session:
        yield session
```

---

## Technologies Deep Dive

### Pydantic Settings
- **What**: Settings management using Pydantic models
- **Why**: Type validation, autocomplete, environment variable parsing
- **Use**: Configuration classes that automatically load from `.env`

### SQLAlchemy
- **What**: Python SQL toolkit and ORM
- **Why**: Database-agnostic, powerful query building, relationship handling
- **Use**: All database operations in the backend

### asyncpg vs psycopg2
- **asyncpg**: Async PostgreSQL driver (for async/await)
- **psycopg2**: Sync PostgreSQL driver (traditional)
- **Our use**: Both via SQLAlchemy (sync for migrations, async for API)

---

## Common Mistakes to Avoid

1. **Committing `.env` to git** - Always gitignore it
2. **Hardcoding database URLs** - Use environment variables
3. **No connection pooling** - Performance will suffer
4. **Wrong URL format** - `postgres://` vs `postgresql://`
5. **No pool_pre_ping** - Stale connections cause errors

---

## Next Steps (Day 2 Preview)

- Docker Compose setup
- PostgreSQL container configuration
- Multi-service orchestration
- Container networking

---

## Quick Reference

**Check database URL:**
```bash
echo $DATABASE_URL
```

**Test database connection:**
```python
from sqlalchemy import create_engine
engine = create_engine(database_url)
conn = engine.connect()
print("Connected!")
```

**Environment variable priority:**
1. System environment variables
2. `.env` file
3. Default values in Settings class
