"""PURPOSE: SQLAlchemy models (Job, Domain, FetchLog) and related schemas.
"""


from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime, JSON, Boolean
from datetime import datetime

# PURPOSE: Define core ORM models for job data.
Base = declarative_base()

class Job(Base):
    __tablename__ = "jobs"
    id: Mapped[str] = mapped_column(String, primary_key=True)  # Upwork job ID
    title: Mapped[str | None] = mapped_column(String, nullable=True)
    domain: Mapped[str | None] = mapped_column(String, nullable=True)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    budget_min: Mapped[int | None] = mapped_column(Integer, nullable=True)
    budget_max: Mapped[int | None] = mapped_column(Integer, nullable=True)
    currency: Mapped[str | None] = mapped_column(String, nullable=True)
    verified_client: Mapped[bool] = mapped_column(Boolean, default=False)
    location: Mapped[str | None] = mapped_column(String, nullable=True)
    posted_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    proposals: Mapped[int | None] = mapped_column(Integer, nullable=True)
    json_raw: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
