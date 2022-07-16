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
def create_wallet(api_key: WalletCreate, db: Session = Depends(get_db)):
    db_wallet = crud.create_wallet(db, wallet=api_key)
    return db_wallet


@walletRouter.post("/deposit_address", response_model=DepositAddress)
def get_deposit_address(deposit_address: DepositAddressCreate, db: Session = Depends(get_db)):
    deposit_address = crud.get_deposit_address(
        db, 
        deposit_address.api_key,
        deposit_address.user_id,
        deposit_address.account_index,
        deposit_address.num_of_addresses,
        deposit_address.blockchain)
    
    return DepositAddress(
        deposit_address,
        blockchain=deposit_address.blockchain,
        user_id=deposit_address.user_id,
        account_index=deposit_address.account_index)

@walletRouter.get("/", response_model=List[WalletCreate])
def get_wallets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    wallets = crud.get_wallets(db, skip=skip, limit=limit)
    return wallets
