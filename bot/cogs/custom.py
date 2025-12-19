import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional

from bot.utils.embeds import success_embed, error_embed


class Custom(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="addcommand", description="Add a custom command")
    @app_commands.checks.has_permissions(administrator=True)
    async def add_command(
        self,
        interaction: discord.Interaction,
        name: str,
        response: str,
        embed: Optional[bool] = False,
    ):
        await interaction.response.defer()
        # Store in database
        collection = self.bot.db.custom_commands
        await collection.update_one(
            {"guild_id": str(interaction.guild.id), "name": name},
            {"$set": {"response": response, "embed": embed}},
            upsert=True,
        )
        embed_msg = success_embed(
            "Custom Command Added", f"Command `{name}` added.", self.bot
        )
        await interaction.followup.send(embed=embed_msg)

    @app_commands.command(name="removecommand", description="Remove a custom command")
    @app_commands.checks.has_permissions(administrator=True)
    async def remove_command(self, interaction: discord.Interaction, name: str):
        await interaction.response.defer()
        collection = self.bot.db.custom_commands
        result = await collection.delete_one(
            {"guild_id": str(interaction.guild.id), "name": name}
        )
        if result.deleted_count:
            embed_msg = success_embed(
                "Custom Command Removed", f"Command `{name}` removed.", self.bot
            )
        else:
            embed_msg = error_embed(
                "Not Found", f"Command `{name}` not found.", self.bot
            )
        await interaction.followup.send(embed=embed_msg)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if not message.content.startswith("!"):
            return
        command_name = message.content[1:].split()[0]
        collection = self.bot.db.custom_commands
        cmd = await collection.find_one(
            {"guild_id": str(message.guild.id), "name": command_name}
        )
        if cmd:
            if cmd.get("embed", False):
                embed_msg = success_embed(
                    command_name.title(), cmd["response"], self.bot
                )
                await message.channel.send(embed=embed_msg)
            else:
                await message.channel.send(cmd["response"])


async def setup(bot):
    await bot.add_cog(Custom(bot))
