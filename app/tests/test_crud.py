import sys
import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

# Ensure the app module can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models import Base, URL
from crud import create_short_url, get_original_url, get_view_count

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="module")
def db():
    """Create a new database session for a test."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_create_short_url(db):
    """Test creating a short URL."""
    url = "https://example.com"
    expiration = 3600  # 1 hour
    short_key = create_short_url(db, url, expiration)
    db_url = db.query(URL).filter(URL.short_key == short_key).first()
    assert db_url is not None
    assert db_url.original_url == url
    assert db_url.short_key == short_key
    assert db_url.expiration is not None

def test_get_original_url(db):
    """Test retrieving the original URL."""
    url = "https://example.com"
    short_key = create_short_url(db, url)
    original_url = get_original_url(db, short_key)
    assert original_url == url

def test_get_view_count(db):
    """Test retrieving the view count."""
    url = "https://example.com"
    short_key = create_short_url(db, url)
    get_original_url(db, short_key)  # Simulate a view
    view_count = get_view_count(db, short_key)
    assert view_count == 1
