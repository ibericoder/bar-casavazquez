import sys
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from sqlalchemy.orm import sessionmaker
from app.core.database import engine
from app.models import User, UserRole
import hashlib

def simple_hash_password(password: str) -> str:
    """Simple password hash for development (don't use in production)"""
    return hashlib.sha256(password.encode()).hexdigest()

def create_admin_user():
    """Create admin user with simple hash"""
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Check if admin user already exists
        existing_admin = session.query(User).filter(User.username == "admin").first()
        if existing_admin:
            print("Admin user already exists")
            return
        
        # Create admin user with simple hash
        admin_user = User(
            username="admin",
            email="admin@casavazquez.com",
            hashed_password=simple_hash_password("admin"),
            full_name="Casa Vazquez Administrator",
            role=UserRole.ADMIN,
            is_active=True
        )
        
        session.add(admin_user)
        session.commit()
        print("Created default admin user:")
        print("  Username: admin")
        print("  Password: admin")
        print("⚠️  IMPORTANT: This uses simple hashing for development only!")
        
    except Exception as e:
        session.rollback()
        print(f"Error creating admin user: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    create_admin_user()