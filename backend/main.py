from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from core.logging import logger
from core.exceptions import setup_exception_handlers
from api.v1.api import api_router

def create_application() -> FastAPI:
    application = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        debug=settings.DEBUG
    )

    setup_exception_handlers(application)

    # CORS configuration
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API routes
    application.include_router(api_router, prefix=settings.API_V1_STR)

    @application.on_event("startup")
    async def startup_event():
        logger.info("Starting up NorthScale Backend...")
        # Validation checks
        validate_environment()

    @application.on_event("shutdown")
    async def shutdown_event():
        logger.info("Shutting down NorthScale Backend...")

    return application

def validate_environment():
    logger.info("Validating environment configurations...")
    required_vars = [
        "SUPABASE_URL",
        "SUPABASE_SERVICE_ROLE_KEY",
        "DATABASE_URL",
        "REDIS_URL",
        "GROQ_API_KEY"
    ]
    missing = []
    for var in required_vars:
        if not getattr(settings, var):
            missing.append(var)
    
    if missing:
        logger.error(f"Missing required environment variables: {', '.join(missing)}")
        # In production we might want to exit here
    else:
        logger.info("Environment validation successful")

app = create_application()

# Root health check (per requirements)
@app.get("/health")
async def root_health():
    return {"status": "ok"}






