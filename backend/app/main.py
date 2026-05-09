from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logging import setup_logging
from app.db.supabase import supabase_client
from app.db.redis import redis_client
from datetime import datetime

# Initialize logging
logger = setup_logging()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Northscale AI Investment Research Terminal API", "v": "1.0.0"}

@app.get("/health")
def health_check():
    # Check Supabase
    supabase_status = "ok" if supabase_client else "error"
    
    # Check Redis
    try:
        redis_status = "ok" if redis_client and redis_client.ping() else "error"
    except:
        redis_status = "error"

    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "supabase": supabase_status,
            "redis": redis_status
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
