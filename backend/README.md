# Casa Vazquez FastAPI Backend

This is the new FastAPI-based backend for Casa Vazquez restaurant, replacing the previous Express.js server with a more robust solution using FastAPI and SQLAlchemy.

## Features

- **FastAPI**: Modern, fast Python web framework
- **SQLAlchemy**: Powerful ORM with database abstraction
- **Pydantic**: Data validation and serialization
- **Database Support**: SQLite (development) and PostgreSQL (production)
- **API Documentation**: Auto-generated with Swagger UI
- **Data Migration**: Scripts to migrate existing data

## Project Structure

```
backend/
├── app/
│   ├── api/          # API endpoints
│   ├── core/         # Core configuration and database
│   ├── models/       # SQLAlchemy models
│   ├── schemas/      # Pydantic schemas
│   └── main.py       # FastAPI application
├── migrations/       # Database migrations
├── init_db.py        # Database initialization
├── migrate_data.py   # Data migration script
├── run.py           # Application runner
├── requirements.txt  # Python dependencies
└── .env             # Environment configuration
```

## Setup and Installation

### 1. Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Initialize Database

```bash
python init_db.py
```

### 3. Migrate Existing Data

```bash
python migrate_data.py
```

### 4. Run the Development Server

```bash
python run.py
```

The API will be available at:
- **API**: http://localhost:8080
- **Documentation**: http://localhost:8080/docs
- **Alternative Docs**: http://localhost:8080/redoc

## API Endpoints

### Wines
- `GET /api/wines/` - Get all wines with filtering
- `GET /api/wines/vinos` - Legacy endpoint for compatibility
- `GET /api/wines/{wine_id}` - Get specific wine
- `POST /api/wines/` - Create new wine
- `PUT /api/wines/{wine_id}` - Update wine
- `DELETE /api/wines/{wine_id}` - Delete wine
- `PATCH /api/wines/{wine_id}/availability` - Toggle availability

### Drinks
- `GET /api/drinks/` - Get all drinks with filtering
- `POST /api/drinks/` - Create new drink
- `PUT /api/drinks/{drink_id}` - Update drink
- `DELETE /api/drinks/{drink_id}` - Delete drink

### Snacks
- `GET /api/snacks/` - Get all snacks with filtering
- `POST /api/snacks/` - Create new snack
- `PUT /api/snacks/{snack_id}` - Update snack
- `DELETE /api/snacks/{snack_id}` - Delete snack

### Notifications
- `GET /api/notifications/` - Get all notifications
- `POST /api/notifications/` - Create new notification
- `PUT /api/notifications/{notification_id}` - Update notification
- `DELETE /api/notifications/{notification_id}` - Delete notification

## Database Models

### Wine
- id, name, color, grape, origin
- short_description, long_description
- image, characteristics, available
- prices (JSON field)

### Drink
- id, name, category, price, volume
- alcoholic, allergens, available
- neu (new item flag)

### Snack
- id, name, price, category, description
- allergens, vegetarian, vegan, available
- neu (new item flag)

### Notification
- id, title, message, type, active
- priority, target_page, expires_at

## Configuration

Environment variables in `.env`:

- `DATABASE_URL`: Database connection string
- `SECRET_KEY`: Security key for API
- `ALLOWED_ORIGINS`: CORS allowed origins
- `ENVIRONMENT`: development/production
- `DEBUG`: Enable debug mode

## Migration from Express.js

The new FastAPI backend is designed to be backward compatible with the existing frontend:

1. **Legacy Endpoint**: `/casavazquez/api/vinos` still works
2. **Static Files**: Serves the Vue.js frontend from `/casavazquez/`
3. **Data Structure**: Maintains the same wine data structure
4. **CORS**: Configured to allow frontend requests

## Production Deployment

For production:

1. Set `DATABASE_URL` to PostgreSQL connection string
2. Set `ENVIRONMENT=production` and `DEBUG=false`
3. Configure proper `SECRET_KEY` and `ALLOWED_ORIGINS`
4. Use a WSGI server like Gunicorn with Uvicorn workers

```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## Development

### Adding New Endpoints

1. Create new router in `app/api/`
2. Define models in `app/models/`
3. Create schemas in `app/schemas/`
4. Include router in `app/main.py`

### Database Changes

1. Modify models in `app/models/`
2. Create migration script or use Alembic
3. Update schemas if needed

## Testing

The API documentation is available at `/docs` for interactive testing of all endpoints.