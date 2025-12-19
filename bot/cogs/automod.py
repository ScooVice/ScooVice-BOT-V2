import discord
from discord.ext import commands
from bot.utils.embeds import warning_embed
import re


class AutoMod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.banned_words = ["badword1", "badword2"]  # Customize this list
        self.spam_threshold = 5  # Messages per 10 seconds
        self.user_messages = {}  # Track user messages for spam

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        # Check for banned words
        if any(word in message.content.lower() for word in self.banned_words):
            await message.delete()
            embed = warning_embed(
                "Banned Word Detected",
                f"{message.author.mention}, your message contained a banned word.",
                self.bot,
            )
            await message.channel.send(embed=embed, delete_after=10)

        # Check for excessive caps (more than 70% caps)
        content = re.sub(r"[^a-zA-Z]", "", message.content)
        if (
            len(content) > 5
            and (sum(1 for c in content if c.isupper()) / len(content)) > 0.7
        ):
            await message.delete()
            embed = warning_embed(
                "Excessive Caps",
                f"{message.author.mention}, please avoid excessive caps.",
                self.bot,
            )
            await message.channel.send(embed=embed, delete_after=10)

        # Check for links (basic)
        if re.search(r"http[s]?://", message.content):
            await message.delete()
            embed = warning_embed(
                "Links Not Allowed",
                f"{message.author.mention}, links are not permitted here.",
                self.bot,
            )
            await message.channel.send(embed=embed, delete_after=10)

        # Basic spam detection
        user_id = message.author.id
        now = message.created_at.timestamp()
        if user_id not in self.user_messages:
            self.user_messages[user_id] = []
        self.user_messages[user_id].append(now)
        # Remove old messages
        self.user_messages[user_id] = [
            t for t in self.user_messages[user_id] if now - t < 10
        ]
        if len(self.user_messages[user_id]) > self.spam_threshold:
            await message.delete()
            embed = warning_embed(
                "Spam Detected",
                f"{message.author.mention}, please stop spamming.",
                self.bot,
            )
            await message.channel.send(embed=embed, delete_after=10)


async def setup(bot):
    await bot.add_cog(AutoMod(bot))
