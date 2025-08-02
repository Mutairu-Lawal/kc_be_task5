import json
import math
from typing import List
from models import Product, CartItem


PRODUCT_FILE = "data/products.json"
CART_FILE = "data/cart.json"


def load_products() -> List[Product]:
    try:
        with open(PRODUCT_FILE, "r") as f:
            data = json.load(f)
            return [Product(**item) for item in data]
    except Exception:
        return []


def load_cart() -> List[CartItem]:
    try:
        with open(CART_FILE, "r") as f:
            data = json.load(f)
            return [CartItem(**item) for item in data]
    except Exception:
        return []


def save_cart(cart: List[CartItem]):
    with open(CART_FILE, "w") as f:
        json.dump([item.dict() for item in cart], f, indent=4)


def add_to_cart(product_id: int, qty: int) -> CartItem:
    products = load_products()
    product = next((p for p in products if p.id == product_id), None)
    if not product:
        raise ValueError("Product not found")

    cart = load_cart()
    for item in cart:
        if item.product_id == product_id:
            item.quantity += qty
            item.total = math.floor(item.quantity * product.price * 100) / 100
            save_cart(cart)
            return item

    total = math.floor(qty * product.price * 100) / 100
    new_item = CartItem(
        product_id=product.id,
        name=product.name,
        price=product.price,
        quantity=qty,
        total=total
    )
    cart.append(new_item)
    save_cart(cart)
    return new_item


def checkout_cart() -> dict:
    cart = load_cart()
    total_amount = sum(item.total for item in cart)
    rounded_total = math.floor(total_amount * 100) / 100
    return {
        "items": cart,
        "total": rounded_total
    }
