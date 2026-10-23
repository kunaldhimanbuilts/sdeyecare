
# from fastapi import FastAPI
# from app.database import Base, engine

# from app.routes import (
#     auth,
#     patient as patient_routes,
#     appointment as appointment_routes,
#     diagnosis as diagnosis_routes,
#     dashboard,
#     user as user_routes,
#     followup,
# )

# from app.models import (
#     user,
#     patient,
#     appointment,
#     diagnosis,
#     diagnosis_v2,
#     prescription,
# )

# import os
# from dotenv import load_dotenv
# from fastapi.middleware.cors import CORSMiddleware

# load_dotenv()

# ENV = os.getenv("ENV", "development")


# app = FastAPI(
#     docs_url=None if ENV == "production" else "/docs",
#     redoc_url=None if ENV == "production" else "/redoc",
#     openapi_url=None if ENV == "production" else "/openapi.json",
# )

# from fastapi.middleware.cors import CORSMiddleware

# Base.metadata.create_all(bind=engine)

# ALLOWED_ORIGINS = [
#     origin.strip()
#     for origin in os.getenv(
#         "ALLOWED_ORIGINS",
#         "http://localhost:5173,http://127.0.0.1:5173"
#     ).split(",")
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=ALLOWED_ORIGINS,
#     allow_credentials=True,
#     allow_methods=[
#         "GET",
#         "POST",
#         "PUT",
#         "PATCH",
#         "DELETE",
#         "OPTIONS",
#     ],
#     allow_headers=[
#         "Authorization",
#         "Content-Type",
#     ],
# )

# app.include_router(auth.router, prefix="/auth", tags=["Auth"])
# app.include_router(
#     patient_routes.router,
#     prefix="/patients",
#     tags=["Patients"],
# )
# app.include_router(
#     appointment_routes.router,
#     prefix="/appointments",
#     tags=["Appointments"],
# )
# app.include_router(
#     diagnosis_routes.router,
#     prefix="/diagnosis",
#     tags=["Diagnosis"],
# )
# app.include_router(followup.router)
# app.include_router(dashboard.router, prefix="/dashboard")
# app.include_router(user_routes.router, prefix="/users", tags=["Users"])



# @app.get("/")
# def home():
#     return {"message": "PDMS Backend Running 🚀"}

# @app.get("/health")
# def health():
#     return {"status": "ok"}

# if __name__ == "__main__":
    
#     import uvicorn

#     uvicorn.run(
#         app,
#         host=os.getenv("HOST", "0.0.0.0"),
#         port=int(os.getenv("PORT", "8000")),
#         reload=False,
#         access_log=True,
#         log_config=None,
#     )


import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine

# API routers
from app.routes import (
    auth,
    patient as patient_routes,
    appointment as appointment_routes,
    diagnosis as diagnosis_routes,
    dashboard,
    user as user_routes,
    followup,
)

# Import models so SQLAlchemy registers their tables.
# Keep these imports until the model and migration audit is complete.
from app.models import (
    user,
    patient,
    appointment,
    diagnosis,
    diagnosis_v2,
    prescription,
)

# Load local .env values for development.
# On Render, configure environment variables in the dashboard.
load_dotenv()

ENV = os.getenv("ENV", "development").strip().lower()
IS_PRODUCTION = ENV == "production"


def get_allowed_origins() -> list[str]:
    """Read explicitly allowed frontend origins."""
    raw_origins = os.getenv("ALLOWED_ORIGINS", "")

    origins = [
        origin.strip().rstrip("/")
        for origin in raw_origins.split(",")
        if origin.strip()
    ]

    if not origins and not IS_PRODUCTION:
        origins = [
            "http://localhost:5173",
            "http://127.0.0.1:5173",
        ]

    if IS_PRODUCTION and not origins:
        raise RuntimeError(
            "ALLOWED_ORIGINS must be configured in production."
        )

    if "*" in origins:
        raise RuntimeError(
            "Wildcard CORS origins are not allowed. "
            "Configure explicit frontend origins."
        )

    return origins


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Do not automatically create or modify database tables at startup.
    # Apply reviewed database migrations before deploying schema changes.
    yield


app = FastAPI(
    title="PDMS API",
    docs_url=None if IS_PRODUCTION else "/docs",
    redoc_url=None if IS_PRODUCTION else "/redoc",
    openapi_url=None if IS_PRODUCTION else "/openapi.json",
    lifespan=lifespan,
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_allowed_origins(),
    allow_credentials=True,
    allow_methods=[
        "GET",
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
        "OPTIONS",
    ],
    allow_headers=[
        "Authorization",
        "Content-Type",
    ],
)

# Register existing API routers.
# Keep these prefixes unchanged to preserve frontend compatibility.
app.include_router(
    auth.router,
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    patient_routes.router,
    prefix="/patients",
    tags=["Patients"],
)

app.include_router(
    appointment_routes.router,
    prefix="/appointments",
    tags=["Appointments"],
)

app.include_router(
    diagnosis_routes.router,
    prefix="/diagnosis",
    tags=["Diagnosis"],
)

app.include_router(followup.router)

app.include_router(
    dashboard.router,
    prefix="/dashboard",
    tags=["Dashboard"],
)

app.include_router(
    user_routes.router,
    prefix="/users",
    tags=["Users"],
)


@app.get("/", tags=["Health"])
def home():
    return {"message": "PDMS Backend Running"}


@app.get("/health", tags=["Health"])
def health():
    # Process health only; this does not verify database connectivity.
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "8000")),
        reload=not IS_PRODUCTION,
        access_log=True,
    )
