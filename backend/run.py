import sys
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

import uvicorn
from app.main import app

if __name__ == "__main__":
    import os
    
    # Use 0.0.0.0 for production (Cloud Run), 127.0.0.1 for local dev
    host = "0.0.0.0" if os.getenv("CLOUD_RUN") else "127.0.0.1"
    reload = os.getenv("CLOUD_RUN") is None
    
    uvicorn.run(
        "app.main:app",
        host=host,
        port=8080,
        reload=reload,
        log_level="info",
        proxy_headers=True,  # Trust X-Forwarded-* headers from Cloud Run
        forwarded_allow_ips="*"  # Allow all IPs (Cloud Run load balancer)
    )