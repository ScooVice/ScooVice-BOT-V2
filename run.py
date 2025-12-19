from dotenv import load_dotenv

load_dotenv()

from bot.main import ScooViceBot
from bot.config import DISCORD_TOKEN

bot = ScooViceBot()
bot.run(DISCORD_TOKEN)
