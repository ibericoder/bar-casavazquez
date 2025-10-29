from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from time import time
from collections import defaultdict

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, calls: int = 100, period: int = 60):
        super().__init__(app)
        self.calls = calls
        self.period = period
        self.clients = defaultdict(list)
    
    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/api/"):
            client = request.client.host
            now = time()
            
            self.clients[client] = [
                req_time for req_time in self.clients[client]
                if now - req_time < self.period
            ]
            
            if len(self.clients[client]) >= self.calls:
                raise HTTPException(status_code=429, detail="Too many requests")
            
            self.clients[client].append(now)
        
        response = await call_next(request)
        return response
