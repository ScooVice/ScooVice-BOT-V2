from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "scoovice_bot_v2")

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]

warnings_col = db["warnings"]

# ========= WARNINGS =========

async def add_warning(guild_id: int, user_id: int, moderator_id: int, reason: str):
    await warnings_col.insert_one({
        "guild_id": guild_id,
        "user_id": user_id,
        "moderator_id": moderator_id,
        "reason": reason,
        "timestamp": datetime.utcnow()
    })

async def count_warnings(guild_id: int, user_id: int) -> int:
    return await warnings_col.count_documents({
        "guild_id": guild_id,
        "user_id": user_id
    })

async def get_warnings(guild_id: int, user_id: int):
    cursor = warnings_col.find(
        {"guild_id": guild_id, "user_id": user_id}
    ).sort("timestamp", 1)
    return await cursor.to_list(length=100)

async def clear_warnings(guild_id: int, user_id: int):
    await warnings_col.delete_many({
        "guild_id": guild_id,
        "user_id": user_id
    })