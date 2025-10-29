"""PURPOSE: Database engine/session initialization and migrations entrypoints.
"""


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings

# PURPOSE: Initialize database engine and session factory.
engine = create_engine(settings.database_url, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
