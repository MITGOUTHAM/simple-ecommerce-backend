from motor.motor_asyncio import AsyncIOMotorClient

# Your connection URI (you can also move it to .env later)
MONGO_URI = "paste your mongo connection uri of driver code here"

# Connect client
client = AsyncIOMotorClient(MONGO_URI)

# Get DB reference
db = client["ecommerce"]  # 🔥 You can change the name if needed
