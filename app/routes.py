from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from sqlalchemy import func

from app import crud
# from sqlalchemy.sql.functions import func
from .schemas import TransactionHash, WalletCreate, DepositAddress, DepositAddressCreate, WithdrawEthereum, WalletBalance, WalletBalanceReq, TransferEthToUser
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

# Transfer etherum to another address


@walletRouter.post("/withdraw_eth", response_model=TransactionHash)
def transfer_etherum(req: WithdrawEthereum, db: Session = Depends(get_db)):
    tx_hash = crud.withdraw_ethereum(
        db,
        req.api_key,
        req.user_id,
        req.to_address,
        req.amount)

    return TransactionHash(hash=tx_hash)

@walletRouter.post("/transfer_eth_to_user", response_model=TransactionHash)
def transfer_eth_to_user(req: TransferEthToUser, db: Session = Depends(get_db)):
    tx_hash = crud.transfer_eth_to_user(
        db=db,
        api_key=req.api_key,
        user_1_id=req.user_1_id,
        user_2_id=req.user_2_id,
        amount=req.amount)

    return TransactionHash(hash=tx_hash)


@walletRouter.post("/balance", response_model=WalletBalance)
def get_balance(req: WalletBalanceReq, db: Session = Depends(get_db)):
    (address, balance) = crud.get_balance(
        db,
        req.api_key,
        req.user_id,
        req.blockchain)

    return WalletBalance(
        blockchain=req.blockchain,
        balance=balance,
        address=address,
        user_id=req.user_id)
