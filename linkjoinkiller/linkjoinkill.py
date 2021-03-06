import re
from typing import Any
import discord
from redbot.core import commands


class LinkJoinKiller(commands.Cog):
    """
    Auto-ban users joining with invites in name.
    """

    __author__ = "mikeshardmind(Sinbad)"
    __version__ = "0.0.2"
    __flavor_text__ = "Not suited for multi-server use version."

    def __init__(self):
        self.regex = re.compile(
            r"<?(https?:\/\/)?(www\.)?(discord\.gg|discordapp\.com\/invite)\b([-a-zA-Z0-9/]*)>?"
        )

    async def on_member_join(self, member):
        if not member.guild.me.guild_permissions.ban_members:
            return
        if self.regex.search(str(member)) is not None:
            x = discord.Object(id=member.id)
            await member.guild.ban(x, reason="invite name")
