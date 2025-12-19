import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))
MONGO_URI = os.getenv("MONGO_URI")

if not DISCORD_TOKEN:
    raise RuntimeError("DISCORD_TOKEN not found in .env")

if not GUILD_ID:
    raise RuntimeError("GUILD_ID not found in .env")

if not MONGO_URI:
    raise RuntimeError("MONGO_URI not found in .env")
