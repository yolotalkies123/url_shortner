# app/app.py
import uvicorn
import os
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
import crud as crud
import models as models
import schemas as schemas
from database import SessionLocal, engine
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint to create shortened URL
@app.post("/shorten", response_model=schemas.URLResponse)
def create_short_url(request: schemas.URLRequest, db: Session = Depends(get_db)):
    short_key = crud.create_short_url(db, request.url, request.expiration)
    short_url = f"{os.getenv('BASE_URL')}/{short_key}"
    return schemas.URLResponse(short_url=short_url)

# Endpoint to redirect to original URL
@app.get("/{short_key}")
def redirect_url(short_key: str, db: Session = Depends(get_db)):
    original_url = crud.get_original_url(db, short_key)
    if original_url:
        return RedirectResponse(url=original_url, status_code=301)
    raise HTTPException(status_code=404, detail="URL not found")

# Endpoint to get URL statistics
@app.get("/stats/{short_key}", response_model=schemas.URLStats)
def get_url_stats(short_key: str, db: Session = Depends(get_db)):
    view_count = crud.get_view_count(db, short_key)
    if view_count is not None:
        return schemas.URLStats(view_count=view_count)
    raise HTTPException(status_code=404, detail="URL not found")

# Ensure tables are created in the database
models.Base.metadata.create_all(bind=engine)
