"""
This is a cog for the settings database
"""

import sqlite3
import discord
from discord.ext import commands

settings_db = sqlite3.connect("settings.db")
settings_cur = settings_db.cursor()
try:
    settings_cur.execute("CREATE TABLE settings(guild, roleIDForPerms)")
    print('created table')
except sqlite3.OperationalError:
    pass  # Table already exists


class SettingsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    command_group = discord.SlashCommandGroup(name="settings")

    @command_group.command()
    async def set(self):
        settings_cur.execute(
            """
            
            """
        )
