from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from sqlalchemy import func

from app import crud
# from sqlalchemy.sql.functions import func
from .schemas import WalletCreate
from .database import get_db

walletRouter = APIRouter(
    prefix="/wallets",
    tags=['Wallets']
)

# @router.get("/", response_model=List[schemas.Post])
@walletRouter.post("/", response_model=WalletCreate)
def create_wallet(api_key: WalletCreate, db: Session = Depends(get_db)):
    db_wallet = crud.create_wallet(db, wallet=api_key)
    return db_wallet

@walletRouter.get("/", response_model=List[WalletCreate])
def get_wallets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    wallets = crud.get_wallets(db, skip=skip, limit=limit)
    return wallets