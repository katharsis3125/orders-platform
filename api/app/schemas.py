from pydantic import BaseModel
from datetime import datetime


class OrderCreate(BaseModel):
    customer_name: str
    product: str


class OrderResponse(BaseModel):
    id: int
    customer_name: str
    product: str
    status: str
    created_at: datetime