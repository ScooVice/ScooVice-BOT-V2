from datetime import datetime, timezone


async def add_warning(db, guild_id: str, user_id: str, reason: str, moderator_id: str):
    collection = db.warnings

    data = {
        "reason": reason,
        "moderator_id": moderator_id,
        "timestamp": datetime.now(timezone.utc),
    }

    await collection.update_one(
        {"guild_id": guild_id, "user_id": user_id},
        {"$push": {"warnings": data}, "$inc": {"count": 1}},
        upsert=True,
    )


async def get_warnings(db, guild_id: str, user_id: str):
    return await db.warnings.find_one({"guild_id": guild_id, "user_id": user_id})


async def clear_warnings(db, guild_id: str, user_id: str):
    await db.warnings.delete_one({"guild_id": guild_id, "user_id": user_id})
