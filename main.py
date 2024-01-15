import discord
import os
import sqlite3

import settings

bot = discord.Bot()

con = sqlite3.connect("points.db")  # https://docs.python.org/3/library/sqlite3.html
cur = con.cursor()
try:
    cur.execute("CREATE TABLE points(guild, user, amount)")
    print('created table')
except sqlite3.OperationalError:
    pass  # Table already exists

cogs = [
    settings.SettingsCog
]


def load_cogs():
    for cog in cogs:
        bot.add_cog(cog(bot))


@bot.listen()
async def on_connect():
    print('Connected!')


@bot.event
async def on_ready():
    print('Ready!')


@bot.command(name='points_add')
async def points_add(ctx, user: discord.User, points: int):
    amount = None  # if it isn't changed, this would be a bug
    ref = cur.execute(f"""SELECT * FROM points
WHERE guild = {ctx.guild.id} AND user={user.id};""")
    fetch_one = ref.fetchone()

    if not fetch_one:
        cur.execute(f"""INSERT INTO points
VALUES ({ctx.guild.id}, {user.id}, {points});""")
    else:
        amount = fetch_one[2] + points
        cur.execute(f"""UPDATE points
SET amount = {amount}
WHERE user={user.id} AND guild={ctx.guild.id};""")
    con.commit()
    embed = discord.Embed(
        title=f"Added {points} points to {user.name}",
        description=f"Current points for user: {amount}",
        color=discord.Color.random()
    )
    await ctx.respond(embed=embed)


@bot.command(name='get_points')
async def get_points(ctx, user: discord.User):
    ref = cur.execute(f"""SELECT * FROM points
WHERE guild = {ctx.guild.id} AND user={user.id};""")
    fetch_one = ref.fetchone()

    if not fetch_one:
        embed = discord.Embed(
            title=f"Info for {user.name}",
            description=f"Error! User is not created.",
            color=discord.Color.red()
        )
        await ctx.respond(embed=embed)
    else:
        embed = discord.Embed(
            title=f"Info for {user.name}",
            description=f"Current points for user: {fetch_one[2]}",
            color=discord.Color.random()
        )
        await ctx.respond(embed=embed)


@bot.command(name='points_remove')  # same as points_add but points are negative
async def points_remove(ctx, user: discord.User, points: int):
    amount = None  # if it isn't changed, this would be a bug
    ref = cur.execute(f"""SELECT * FROM points
WHERE guild = {ctx.guild.id} AND user={user.id};""")
    fetch_one = ref.fetchone()

    points = -points

    if not fetch_one:
        cur.execute(f"""INSERT INTO points
VALUES ({ctx.guild.id}, {user.id}, {points});""")
    else:
        amount = fetch_one[2] + points
        cur.execute(f"""UPDATE points
SET amount = {amount}
WHERE user={user.id} AND guild={ctx.guild.id};""")
    con.commit()
    embed = discord.Embed(
        title=f"Added {points} points to {user.name}",
        description=f"Current points for user: {amount}",
        color=discord.Color.random()
    )
    await ctx.respond(embed=embed)


@bot.command(name='points_reset')
async def points_reset(ctx, user: discord.User):
    amount = None  # if it isn't changed, this would be a bug
    ref = cur.execute(f"""SELECT * FROM points
WHERE guild = {ctx.guild.id} AND user={user.id};""")
    fetch_one = ref.fetchone()

    if not fetch_one:
        embed = discord.Embed(
            title=f"Info for {user.name}",
            description=f"Error! User is not created.",
            color=discord.Color.red()
        )
        await ctx.respond(embed=embed)
    else:
        amount = fetch_one[2]
        cur.execute(f"""UPDATE points
SET amount = 0
WHERE user={user.id} AND guild={ctx.guild.id};""")
    con.commit()
    embed = discord.Embed(
        title=f"Reset {amount} points for {user.name}",
        description=f"Current points for user: 0",
        color=discord.Color.random()
    )
    await ctx.respond(embed=embed)

load_cogs()
bot.run(str(os.getenv('BOT_TOKEN')))
