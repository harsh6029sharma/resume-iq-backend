from app.db.config import Base
from sqlalchemy.orm import mapped_column, relationship, Mapped
from sqlalchemy import String, Boolean, DateTime, ForeignKey, Text, Integer, Float, JSON, func
from datetime import datetime, timezone
from typing import List, Optional

class User(Base):
    __tablename__ = "user"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        onupdate=func.now()
    )

    # relationships
    refresh_token: Mapped[List["RefreshToken"]] = relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan")
    jobs: Mapped[List["Job"]] = relationship("Job", back_populates="user")
    analyses: Mapped[List["Analysis"]] = relationship("Analysis", back_populates="user")
    candidates: Mapped[List["Candidate"]] = relationship("Candidate", back_populates="user")


class RefreshToken(Base):
    __tablename__ = "refresh_token"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), index=True)
    token: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    revoked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="refresh_token")


class Job(Base):
    __tablename__ = "jobs"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    
    job_title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped["User"] = relationship("User", back_populates="jobs")
    analyses: Mapped[List["Analysis"]] = relationship("Analysis", back_populates="job", cascade="all, delete-orphan")


class Candidate(Base):
    __tablename__ = "candidates"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    name: Mapped[Optional[str]] = mapped_column(String(255))
    resume_text: Mapped[str] = mapped_column(Text, nullable=False)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped["User"] = relationship("User", back_populates="candidates")
    analyses: Mapped[List["Analysis"]] = relationship("Analysis", back_populates="candidate", cascade="all, delete-orphan")


class Analysis(Base):
    __tablename__ = "analyses"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.id", ondelete="CASCADE"))
    candidate_id: Mapped[int] = mapped_column(ForeignKey("candidates.id", ondelete="CASCADE"))

    score: Mapped[float] = mapped_column(Float, nullable=False)
    full_feedback: Mapped[dict] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped["User"] = relationship("User", back_populates="analyses")
    job: Mapped["Job"] = relationship("Job", back_populates="analyses")
    candidate: Mapped["Candidate"] = relationship("Candidate", back_populates="analyses")