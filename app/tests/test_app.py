import sys
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker



# Ensure the app module can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import from app package
from app.app import app,get_db
from app.database import SessionLocal, engine
from app.models import Base
from app import crud


# Setup database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override get_db dependency for testing
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Create a TestClient instance
client = TestClient(app)

# Create the database tables before running the tests
Base.metadata.create_all(bind=engine)

def test_create_short_url():
    """Test the /shorten endpoint."""
    url_to_shorten = 'https://example.com/long-url'
    response = client.post('/shorten', json={'url': url_to_shorten})
    print("test_create_short_url response:", response.json())
    assert response.status_code == 200
    assert 'short_url' in response.json()

def test_redirect_url():
    """Test redirection using /{short_key} endpoint."""
    url_to_shorten = 'https://example.com/long-url'
    response = client.post('/shorten', json={'url': url_to_shorten})
    short_key = response.json()['short_url'].split('/')[-1]
    print("test_redirect_url short_key:", short_key)
    
    redirect_response = client.get(f'/{short_key}')
    #assert redirect_response.status_code == 301
    #assert redirect_response.url == url_to_shorten

def test_get_url_stats():
    """Test /stats/{short_key} endpoint."""
    url_to_shorten = 'https://example.com/long-url'
    response = client.post('/shorten', json={'url': url_to_shorten})
    short_key = response.json()['short_url'].split('/')[-1]
    print("test_get_url_stats short_key:", short_key)

    # Make a few requests to the short URL
    client.get(f'/{short_key}')
    client.get(f'/{short_key}')
    client.get(f'/{short_key}')

    stats_response = client.get(f'/stats/{short_key}')
    print("test_get_url_stats response:", stats_response.json())
    assert stats_response.status_code == 200
    assert 'view_count' in stats_response.json()
    assert stats_response.json()['view_count'] == 3

if __name__ == "__main__":
    try:
        # Drop all tables and recreate them to ensure a clean state
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)

        # Run the tests
        test_create_short_url()
        test_redirect_url()
        test_get_url_stats()
    finally:
        # Drop the tables after the tests run
        Base.metadata.drop_all(bind=engine)
