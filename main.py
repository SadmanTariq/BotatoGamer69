import discord
from discord.ext import commands
from os import environ

TOKEN_VARIABLE_NAME = "DISCORD_TOKEN"
token = ""
try:
    token = environ[TOKEN_VARIABLE_NAME]
except KeyError:
    print("Token variable not set. Quitting.")
    quit()


bot = commands.Bot(command_prefix='>')
currently_running_games = []


@bot.command()
async def duel(ctx, game_name: str, target: discord.Member):
    await ctx.send(f"{ctx.author.mention} challenges {target.mention} to a " +
                   f"game of {game_name}!")


@bot.listen()
async def on_ready():
    print("Ready.")

bot.run(token)
