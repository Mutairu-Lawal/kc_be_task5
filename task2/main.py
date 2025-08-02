from fastapi import FastAPI, HTTPException, Query
from cart import load_products, add_to_cart, checkout_cart
from models import Product, CartItem
from typing import List


app = FastAPI(title="Mini Shopping Cart API")


@app.get("/products/", response_model=List[Product])
def get_products():
    return load_products()


@app.post("/cart/add", response_model=CartItem)
def add_cart(product_id: int = Query(...), qty: int = Query(...)):
    try:
        if qty <= 0:
            raise HTTPException(status_code=400, detail="Quantity must be > 0")
        item = add_to_cart(product_id, qty)
        return item
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/cart/checkout")
def checkout():
    try:
        return checkout_cart()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
