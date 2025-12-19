import discord
from discord.ext import commands
from bot.utils.embeds import info_embed


class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        log_channel = discord.utils.get(guild.channels, name="mod-logs")
        if log_channel:
            embed = info_embed(
                "Member Banned", f"**User:** {user}\n**ID:** {user.id}", self.bot
            )
            await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        log_channel = discord.utils.get(guild.channels, name="mod-logs")
        if log_channel:
            embed = info_embed(
                "Member Unbanned", f"**User:** {user}\n**ID:** {user.id}", self.bot
            )
            await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        # Check if kicked (basic, as discord.py doesn't have direct kick event)
        # For better accuracy, log in kick command
        pass

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.timed_out_until != after.timed_out_until:
            log_channel = discord.utils.get(after.guild.channels, name="mod-logs")
            if log_channel:
                if after.timed_out_until:
                    embed = info_embed(
                        "Member Muted",
                        f"**User:** {after}\n**Until:** {after.timed_out_until}",
                        self.bot,
                    )
                else:
                    embed = info_embed("Member Unmuted", f"**User:** {after}", self.bot)
                await log_channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Logs(bot))
