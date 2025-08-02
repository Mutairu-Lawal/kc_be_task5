from pydantic import BaseModel


class Product(BaseModel):
    id: int
    name: str
    price: float


class CartItem(BaseModel):
    product_id: int
    name: str
    price: float
    quantity: int
    total: float
