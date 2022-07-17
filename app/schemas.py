from enum import Enum
from typing import List, Union

from pydantic import BaseModel


class WalletBase(BaseModel):
    api_key: str


class WalletBalance(BaseModel):
    blockchain: str
    balance: int
    address: str
    user_id: int


class WalletBalanceReq(BaseModel):
    api_key: str
    user_id: int
    blockchain: str


class WalletCreate(WalletBase):
    class Config:
        orm_mode = True


class BlockchainEnum(str, Enum):
    ethereum = "eth"
    solana = "sol"


class DepositAddressCreate(BaseModel):
    api_key: str
    user_id: int
    account_index: int
    num_of_addresses: int
    # ethereum or solana
    blockchain: BlockchainEnum


class DepositAddress(BaseModel):
    address: str
    blockchain: str
    user_id: int
    account_index: int


class TransactionHash(BaseModel):
    hash: str


class WithdrawEthereum(BaseModel):
    api_key: str
    user_id: int
    to_address: str
    amount: str


class ItemBase(BaseModel):
    title: str
    description: Union[str, None] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: List[Item] = []

    class Config:
        orm_mode = True
