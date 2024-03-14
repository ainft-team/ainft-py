from pydantic import BaseModel
from typing import Any, List, Literal, Optional, Union

SetMultiOperationType = Literal["SET"]
GetMultiOperationType = Literal["GET"]
SetOperationType = Literal["SET_VALUE", "INC_VALUE", "DEC_VALUE", "SET_RULE", "SET_OWNER", "SET_FUNCTION"]
GetOperationType = Literal["GET_VALUE", "GET_RULE", "GET_OWNER", "GET_FUNCTION"]


class SetOperation(BaseModel):
    type: SetOperationType
    ref: str
    value: Optional[Any] = None


class SetMultiOperation(BaseModel):
    type: SetMultiOperationType
    op_list: List[SetOperation]


class TransactionInput(BaseModel):
    operation: Union[SetOperation, SetMultiOperation]
    timestamp: int
    nonce: Optional[int] = None
    address: Optional[str] = None
    gas_price: Optional[int] = None


class Thread(BaseModel):
    id: str
    metadata: Optional[object] = None
    created_at: int


class TransactionResult(BaseModel):
    tx_hash: str
    result: dict


class ThreadTransactionResult(TransactionResult):
    thread: Thread
