from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from sqlalchemy import func

from app import crud
# from sqlalchemy.sql.functions import func
from .schemas import WalletCreate, DepositAddress, DepositAddressCreate
from .database import get_db

walletRouter = APIRouter(
    prefix="/wallets",
    tags=['Wallets']
)

# @router.get("/", response_model=List[schemas.Post])


@walletRouter.post("/", response_model=WalletCreate)
def create_wallet(db: Session = Depends(get_db)):
    db_wallet = crud.create_wallet(db=db)
    return db_wallet


@walletRouter.post("/deposit_address", response_model=DepositAddress)
def get_deposit_address(req: DepositAddressCreate, db: Session = Depends(get_db)):
    deposit_address = crud.get_deposit_address(
        db, 
        req.api_key,
        req.user_id,
        req.account_index,
        req.num_of_addresses,
        req.blockchain)
    
    return DepositAddress(
        address=deposit_address,
        blockchain=req.blockchain,
        user_id=req.user_id,
        account_index=req.account_index)

@walletRouter.get("/", response_model=List[WalletCreate])
def get_wallets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    wallets = crud.get_wallets(db, skip=skip, limit=limit)
    return wallets
