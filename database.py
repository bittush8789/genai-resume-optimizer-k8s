from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./resume_analyzer.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100), unique=True, index=True)
    password_hash = Column(String(200))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    resumes = relationship("Resume", back_populates="owner")
    reports = relationship("Report", back_populates="owner")

class Resume(Base):
    __tablename__ = "resumes"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    filename = Column(String(255))
    parsed_text = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    owner = relationship("User", back_populates="resumes")

class Report(Base):
    __tablename__ = "reports"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    resume_id = Column(Integer, ForeignKey("resumes.id"))
    ats_score = Column(Float)
    match_score = Column(Float)
    missing_keywords = Column(Text)  # JSON string
    suggestions = Column(Text)
    job_description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    owner = relationship("User", back_populates="reports")

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
