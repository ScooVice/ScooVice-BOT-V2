from datetime import datetime, timezone


async def log_action(
    db, guild_id: str, user_id: str, action: str, reason: str, moderator_id: str
):
    await db.modlogs.insert_one(
        {
            "guild_id": guild_id,
            "user_id": user_id,
            "action": action,
            "reason": reason,
            "moderator_id": moderator_id,
            "timestamp": datetime.now(timezone.utc),
        }
    )


async def get_logs(
    db,
    guild_id: str,
    user_id: str | None = None,
    action: str | None = None,
    limit: int = 10,
):
    query = {"guild_id": guild_id}

    if user_id:
        query["user_id"] = user_id
    if action:
        query["action"] = action

    cursor = db.modlogs.find(query).sort("timestamp", -1).limit(limit)
    return await cursor.to_list(length=limit)
