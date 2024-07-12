# app/crud.py
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import models as models
import utils as utils

def create_short_url(db: Session, url: str, expiration: int = None):
    short_key = utils.generate_short_key()
    expiration_time = None
    if expiration:
        expiration_time = datetime.utcnow() + timedelta(seconds=expiration)

    db_url = models.URL(original_url=url, short_key=short_key, expiration=expiration_time)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return short_key

def get_original_url(db: Session, short_key: str):
    db_url = db.query(models.URL).filter(models.URL.short_key == short_key).first()
    if db_url and (db_url.expiration is None or db_url.expiration > datetime.utcnow()):
        db_url.view_count += 1
        db.commit()
        db.refresh(db_url)
        return db_url.original_url
    return None

def get_view_count(db: Session, short_key: str):
    db_url = db.query(models.URL).filter(models.URL.short_key == short_key).first()
    if db_url:
        return db_url.view_count
    return None
