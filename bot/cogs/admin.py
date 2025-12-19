import discord
from discord import app_commands
from discord.ext import commands
from datetime import timedelta
from typing import Optional

from bot.utils.embeds import success_embed, error_embed, warning_embed
from bot.database.modlogs import log_action
from bot.database.warnings import add_warning, get_warnings, clear_warnings


class Admin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = bot.db  # pastiin di main.py bot.db = database

    # =========================
    # KICK
    # =========================
    @app_commands.command(name="kick", description="Kick a member from the server")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: Optional[str] = "No reason provided",
    ):
        await interaction.response.defer()

        if member == interaction.user:
            await interaction.followup.send(
                embed=error_embed(
                    "Action denied", "You cannot kick yourself.", self.bot
                ),
                ephemeral=True,
            )
            return

        if member.top_role >= interaction.guild.me.top_role:
            await interaction.followup.send(
                embed=error_embed(
                    "Hierarchy error", "I cannot kick this member.", self.bot
                ),
                ephemeral=True,
            )
            return

        await member.kick(reason=reason)

        await log_action(
            self.db,
            str(interaction.guild.id),
            str(member.id),
            "kick",
            reason,
            str(interaction.user.id),
        )

        await interaction.followup.send(
            embed=success_embed(
                "Member kicked", f"**User:** {member}\n**Reason:** {reason}", self.bot
            )
        )

    # =========================
    # BAN
    # =========================
    @app_commands.command(name="ban", description="Ban a member from the server")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: Optional[str] = "No reason provided",
    ):
        await interaction.response.defer()

        if member == interaction.user:
            await interaction.followup.send(
                embed=error_embed(
                    "Action denied", "You cannot ban yourself.", self.bot
                ),
                ephemeral=True,
            )
            return

        if member.top_role >= interaction.guild.me.top_role:
            await interaction.followup.send(
                embed=error_embed(
                    "Hierarchy error", "I cannot ban this member.", self.bot
                ),
                ephemeral=True,
            )
            return

        await interaction.guild.ban(member, reason=reason)

        await log_action(
            self.db,
            str(interaction.guild.id),
            str(member.id),
            "ban",
            reason,
            str(interaction.user.id),
        )

        await interaction.followup.send(
            embed=success_embed(
                "Member banned", f"**User:** {member}\n**Reason:** {reason}", self.bot
            )
        )

    # =========================
    # UNBAN
    # =========================
    @app_commands.command(name="unban", description="Unban a user by ID")
    @app_commands.checks.has_permissions(ban_members=True)
    async def unban(
        self,
        interaction: discord.Interaction,
        user_id: str,
        reason: Optional[str] = "No reason provided",
    ):
        await interaction.response.defer()

        user = await self.bot.fetch_user(int(user_id))
        await interaction.guild.unban(user, reason=reason)

        await log_action(
            self.db,
            str(interaction.guild.id),
            str(user.id),
            "unban",
            reason,
            str(interaction.user.id),
        )

        await interaction.followup.send(
            embed=success_embed(
                "User unbanned", f"**User:** {user}\n**Reason:** {reason}", self.bot
            )
        )

    # =========================
    # TEMP BAN
    # =========================
    @app_commands.command(name="tempban", description="Temporarily ban a member")
    @app_commands.checks.has_permissions(ban_members=True)
    async def tempban(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        days: int,
        reason: Optional[str] = "No reason provided",
    ):
        await interaction.response.defer()

        if member == interaction.user:
            await interaction.followup.send(
                embed=error_embed(
                    "Action denied", "You cannot ban yourself.", self.bot
                ),
                ephemeral=True,
            )
            return

        if member.top_role >= interaction.guild.me.top_role:
            await interaction.followup.send(
                embed=error_embed(
                    "Hierarchy error", "I cannot ban this member.", self.bot
                ),
                ephemeral=True,
            )
            return

        duration = timedelta(days=days)
        await member.ban(reason=reason, delete_message_days=0)

        # Schedule unban
        import asyncio

        async def unban_after():
            await asyncio.sleep(duration.total_seconds())
            await interaction.guild.unban(member)

        self.bot.loop.create_task(unban_after())

        await log_action(
            self.db,
            str(interaction.guild.id),
            str(member.id),
            "tempban",
            reason,
            str(interaction.user.id),
        )

        await interaction.followup.send(
            embed=success_embed(
                "Member temporarily banned",
                f"**User:** {member}\n**Duration:** {days} days\n**Reason:** {reason}",
                self.bot,
            )
        )

    # =========================
    # MUTE (TIMEOUT)
    # =========================
    @app_commands.command(name="mute", description="Timeout a member")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def mute(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        minutes: int,
        reason: Optional[str] = "No reason provided",
    ):
        await interaction.response.defer()

        if member == interaction.user:
            await interaction.followup.send(
                embed=error_embed(
                    "Action denied", "You cannot mute yourself.", self.bot
                ),
                ephemeral=True,
            )
            return

        if member.top_role >= interaction.guild.me.top_role:
            await interaction.followup.send(
                embed=error_embed(
                    "Hierarchy error", "I cannot mute this member.", self.bot
                ),
                ephemeral=True,
            )
            return

        duration = timedelta(minutes=minutes)
        await member.timeout(duration, reason=reason)

        await log_action(
            self.db,
            str(interaction.guild.id),
            str(member.id),
            "mute",
            reason,
            str(interaction.user.id),
        )

        await interaction.followup.send(
            embed=warning_embed(
                "Member muted",
                f"**User:** {member}\n**Duration:** {minutes} minutes\n**Reason:** {reason}",
                self.bot,
            )
        )

    # =========================
    # UNMUTE
    # =========================
    @app_commands.command(name="unmute", description="Remove timeout from a member")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def unmute(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: Optional[str] = "No reason provided",
    ):
        await interaction.response.defer()

        await member.timeout(None)

        await log_action(
            self.db,
            str(interaction.guild.id),
            str(member.id),
            "unmute",
            reason,
            str(interaction.user.id),
        )

        await interaction.followup.send(
            embed=success_embed(
                "Member unmuted", f"**User:** {member}\n**Reason:** {reason}", self.bot
            )
        )

    # =========================
    # WARN
    # =========================
    @app_commands.command(name="warn", description="Warn a member")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def warn(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: Optional[str] = "No reason provided",
    ):
        await interaction.response.defer()

        if member == interaction.user:
            await interaction.followup.send(
                embed=error_embed(
                    "Action denied", "You cannot warn yourself.", self.bot
                ),
                ephemeral=True,
            )
            return

        if member.top_role >= interaction.guild.me.top_role:
            await interaction.followup.send(
                embed=error_embed(
                    "Hierarchy error", "I cannot warn this member.", self.bot
                ),
                ephemeral=True,
            )
            return

        await add_warning(
            self.db,
            str(interaction.guild.id),
            str(member.id),
            reason,
            str(interaction.user.id),
        )

        data = await get_warnings(self.db, str(interaction.guild.id), str(member.id))
        count = data["count"] if data else 0

        await log_action(
            self.db,
            str(interaction.guild.id),
            str(member.id),
            "warn",
            reason,
            str(interaction.user.id),
        )

        # AUTO MUTE AT 3 WARNS
        if count >= 3:
            await member.timeout(timedelta(hours=1), reason="Auto mute: 3 warnings")

            await log_action(
                self.db,
                str(interaction.guild.id),
                str(member.id),
                "auto-mute",
                "Reached 3 warnings",
                str(self.bot.user.id),
            )

            # Reset warnings after auto-mute
            await clear_warnings(self.db, str(interaction.guild.id), str(member.id))

        await interaction.followup.send(
            embed=warning_embed(
                "Member warned",
                f"**User:** {member}\n**Warnings:** {count}/3\n**Reason:** {reason}",
                self.bot,
            )
        )

    # =========================
    # WARNINGS
    # =========================
    @app_commands.command(name="warnings", description="View warnings of a member")
    async def warnings(self, interaction: discord.Interaction, member: discord.Member):
        await interaction.response.defer(ephemeral=True)

        data = await get_warnings(self.db, str(interaction.guild.id), str(member.id))

        count = data["count"] if data else 0

        await interaction.followup.send(
            embed=warning_embed(
                "Warnings info",
                f"**User:** {member}\n**Warnings:** {count}/3",
                self.bot,
            )
        )

    # =========================
    # CLEAR WARNINGS
    # =========================
    @app_commands.command(
        name="clearwarnings", description="Clear all warnings of a member"
    )
    @app_commands.checks.has_permissions(moderate_members=True)
    async def clearwarnings(
        self, interaction: discord.Interaction, member: discord.Member
    ):
        await interaction.response.defer()

        await clear_warnings(self.db, str(interaction.guild.id), str(member.id))

        await log_action(
            self.db,
            str(interaction.guild.id),
            str(member.id),
            "clearwarnings",
            "Warnings cleared",
            str(interaction.user.id),
        )

        await interaction.followup.send(
            embed=success_embed(
                "Warnings cleared", f"All warnings cleared for **{member}**", self.bot
            )
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(Admin(bot))
