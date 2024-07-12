# app/models.py
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from sqlalchemy.orm import declarative_base
Base = declarative_base()

class URL(Base):
    __tablename__ = "urls_hub"
    
    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, index=True)
    short_key = Column(String, unique=True, index=True)
    expiration = Column(DateTime, nullable=True)
    view_count = Column(Integer, default=0)
