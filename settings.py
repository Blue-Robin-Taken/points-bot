"""
This is a cog for the settings database
"""

import sqlite3
import discord
from discord.ext import commands
import discord.ui
from discord.ui import View, Select

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

    @staticmethod
    def convert_list_to_options(input_list):
        return [discord.OptionChoice(name=option) for option in input_list]

    class PermRoleSelect(Select):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)

        async def callback(self, interaction):
            if interaction.user.guild_permissions.administrator:
                ref = settings_cur.execute(
                    f"""
                            SELECT * FROM settings
                WHERE guild = {interaction.guild.id};"""
                )
                fetch_one = ref.fetchone()
                if not fetch_one:
                    settings_cur.execute(f"""INSERT INTO settings
                    VALUES ({interaction.guild.id}, {self.values[0].id});""")
                else:
                    settings_cur.execute(f"""UPDATE settings
                    SET roleIDForPerms = {self.values[0].id}
                    WHERE guild={interaction.guild.id};""")
                settings_db.commit()
                await interaction.response.send_message("test")

            else:
                await interaction.response.send_message("You need administrator privileges to access this.",
                                                        ephemeral=True)

    @command_group.command()
    async def set(self, ctx, choice_type: discord.Option(str, choices=convert_list_to_options(["PermRoles"]))):
        if ctx.user.guild_permissions.administrator:

            if choice_type == "PermRoles":
                view = View()
                select = self.PermRoleSelect(select_type=discord.ComponentType.role_select)
                view.add_item(select)
                await ctx.respond("Select a role", view=view)
            else:
                await ctx.respond("Error")

        else:
            await ctx.respond("You need administrator privileges to access this.", ephemeral=True)

    @command_group.command()
    async def view(self, ctx):
        if ctx.user.guild_permissions.administrator:
            ref = settings_cur.execute(
                f"""
                        SELECT * FROM settings
            WHERE guild = {ctx.guild.id};"""
            )
            fetch_one = ref.fetchone()
            embed = discord.Embed(
                title=f"Settings for {ctx.guild.name}",
                description=f"Role ID for accessing points logger: {fetch_one[1]}",
                color=discord.Color.random()
            )
            embed.set_footer(text="If you wanted to ping the role, it would be <@&(roleid)>")
            await ctx.respond(embed=embed)
        else:
            await ctx.respond("You need administrator privileges to access this.", ephemeral=True)
