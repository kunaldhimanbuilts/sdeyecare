# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, declarative_base
# import os
# import sys
# from dotenv import load_dotenv
# from sqlalchemy.exc import SQLAlchemyError

# from fastapi import HTTPException
# from sqlalchemy.exc import OperationalError





# # 🔥 FIX FOR BOTH DEV + EXE
# if getattr(sys, 'frozen', False):
#     # running as EXE
#     BASE_DIR = os.path.dirname(sys.executable)
# else:
#     # running normally
#     BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# env_path = os.path.join(BASE_DIR, ".env")

# print("Loading .env from:", env_path)  # debug

# load_dotenv(env_path)

# DATABASE_URL = os.getenv("DATABASE_URL")

# if not DATABASE_URL:
#     raise ValueError(f"DATABASE_URL not found in .env at {env_path}")


# try:
#     engine = create_engine(
#         DATABASE_URL,
#         pool_pre_ping=True,
#         pool_recycle=300,
#     )
# except SQLAlchemyError as e:
#     print(f"Database connection failed: {e}")
#     raise

# # SessionLocal = sessionmaker(bind=engine)
# SessionLocal = sessionmaker(
#     autocommit=False,
#     autoflush=False,
#     bind=engine,
# )
# Base = declarative_base()

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     except OperationalError:
#         raise HTTPException(
#             status_code=503,
#             detail="Database is unavailable."
#         )
#     finally:
#         db.close()





import os
import sys

from dotenv import load_dotenv
from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from sqlalchemy.orm import declarative_base, sessionmaker


# Locate .env for local development and packaged desktop builds.
if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

env_path = os.path.join(BASE_DIR, ".env")

# Do not override environment variables already configured by Render.
load_dotenv(env_path, override=False)

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is not configured. Set it in the deployment "
        "environment or provide a local .env file."
    )

# Normalize common PostgreSQL URL formats for psycopg2.
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgres://", "postgresql://", 1
    )

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=5,
    max_overflow=5,
    pool_timeout=30,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


def get_db():
    db = SessionLocal()

    try:
        yield db
    except OperationalError as exc:
        db.rollback()
        raise HTTPException(
            status_code=503,
            detail="Database is temporarily unavailable.",
        ) from exc
    except SQLAlchemyError:
        db.rollback()
        raise
    finally:
        db.close()
