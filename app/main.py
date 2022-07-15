from sqlalchemy import null

from app import schemas
from .database import engine
from . import models
from . import schemas
import os
from fastapi import FastAPI, Response, status, HTTPException, Depends
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from .database import SessionLocal, engine


load_dotenv()  # take environment variables from .env.


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.get("/items", response_model=list[schemas.Item])
def get_items(db: Session = Depends(get_db)):
    items = db.query(models.Item).all()
    print(items)
    return items

