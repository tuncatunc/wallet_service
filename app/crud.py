import secrets
from fastapi import HTTPException
from sqlalchemy.orm import Session
from py_crypto_hd_wallet import \
    HdWalletBipFactory, \
    HdWalletSaver, \
    HdWalletBip44Coins, \
    HdWalletBipWordsNum, \
    HdWalletBipDataTypes

from . import models
from . import schemas


def create_wallet(db: Session):
    hd_wallet_fact = HdWalletBipFactory(HdWalletBip44Coins.ETHEREUM)
    hd_wallet = hd_wallet_fact.CreateRandom(
        "Ethereum Wallet", HdWalletBipWordsNum.WORDS_NUM_24)

    wallet_mnemonic = hd_wallet.GetData(HdWalletBipDataTypes.MNEMONIC)
    api_key = secrets.token_urlsafe(32)
    db_wallet = models.Wallet(api_key=api_key, wallet_mnemonic=wallet_mnemonic)

    db.add(db_wallet)
    db.commit()
    db.refresh(db_wallet)
    return {"api_key": db_wallet.api_key}


def get_deposit_address(
        db: Session,
        api_key: str,
        user_id: int,
        user_account_index: int,
        num_of_addresses=1,
        blockchain: str = "ETH"):
    db_wallet = db.query(models.Wallet).filter(
        models.Wallet.api_key == api_key).first()
    if db_wallet is None:
        raise HTTPException(status_code=404, detail="Wallet not found")

    hd_wallet_fact = HdWalletBipFactory(HdWalletBip44Coins.ETHEREUM)
    hd_wallet = hd_wallet_fact.CreateFromMnemonic(
        wallet_name="wallet_name",
        mnemonic=db_wallet.wallet_mnemonic)

    hd_wallet.Generate(acc_idx=user_account_index,
                       addr_num=num_of_addresses, addr_off=0)
    # address = hd_wallet.GetKey(HdWalletBipDataTypes.ADDRESS)

    return hd_wallet.GetData(HdWalletBipDataTypes.ADDRESS).ToDict()["address_0"]["address"]


def get_wallets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Wallet).offset(skip).limit(limit).all()

# def get_user(db: Session, user_id: int):
#     return db.query(models.User).filter(models.User.id == user_id).first()


# def get_user_by_email(db: Session, email: str):
#     return db.query(models.User).filter(models.User.email == email).first()


# def get_users(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.User).offset(skip).limit(limit).all()


# def create_user(db: Session, user: schemas.UserCreate):
#     fake_hashed_password = user.password + "notreallyhashed"
#     db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user


# def get_items(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Item).offset(skip).limit(limit).all()


# def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
#     db_item = models.Item(**item.dict(), owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item
