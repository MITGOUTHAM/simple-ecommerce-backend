from fastapi import APIRouter, Query
from app.schemas.product import ProductCreate
from app.db import db
import uuid

router = APIRouter()

@router.post("/products", status_code=201)
async def create_product(product: ProductCreate):
    product_id = str(uuid.uuid4())

    product_doc = {
        "_id": product_id,
        "name": product.name,
        "price": product.price,
        "sizes": [s.dict() for s in product.sizes]
    }

    await db.products.insert_one(product_doc)

    return {"id": product_id}


@router.get("/products")
async def list_products(
    name: str = Query(None),
    size: str = Query(None),
    limit: int = 10,
    offset: int = 0
):
    query = {}

    if name:
        query["name"] = {"$regex": name, "$options": "i"}
    if size:
        query["sizes"] = {"$elemMatch": {"size": size}}

    cursor = db.products.find(query).skip(offset).limit(limit)
    products = await cursor.to_list(length=limit)

    return {
        "data": [
            {
                "id": p["_id"],
                "name": p["name"],
                "price": p["price"]
            } for p in products
        ],
        "page": {
            "next": str(offset + limit),
            "limit": limit,
            "previous": str(max(offset - limit, 0))
        }
    }
