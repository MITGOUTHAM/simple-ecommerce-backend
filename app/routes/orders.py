from fastapi import APIRouter, HTTPException
from app.schemas.order import OrderCreate
from app.db import db
import uuid

router = APIRouter()

@router.post("/orders", status_code=201)
async def create_order(order: OrderCreate):
    order_id = str(uuid.uuid4())
    total = 0
    items = []

    for item in order.items:
        product = await db.products.find_one({"_id": item.productId})
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.productId} not found")

        items.append({
            "productDetails": {
                "id": product["_id"],
                "name": product["name"]
            },
            "qty": item.qty
        })

        total += item.qty * 100  # Replace with actual product['price'] if needed

    order_doc = {
        "_id": order_id,
        "user_id": order.userId,
        "items": items,
        "total": total
    }

    await db.orders.insert_one(order_doc)

    return {"id": order_id}


@router.get("/orders/{user_id}")
async def get_orders(user_id: str, limit: int = 10, offset: int = 0):
    cursor = db.orders.find({"user_id": user_id}).skip(offset).limit(limit)
    orders = await cursor.to_list(length=limit)

    return {
        "data": [
            {
                "id": o["_id"],
                "user_id": o["user_id"],
                "items": o["items"],
                "total": o["total"]
            } for o in orders
        ],
        "page": {
            "next": str(offset + limit),
            "limit": limit,
            "previous": str(max(offset - limit, 0))
        }
    }
