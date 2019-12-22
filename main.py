import discord
from discord.ext import commands
from os import environ
import minigames.brawler


TOKEN_VARIABLE_NAME = "DISCORD_TOKEN"
token = ""
try:
    token = environ[TOKEN_VARIABLE_NAME]
except KeyError:
    print("Token variable not set. Quitting.")
    quit()


bot = commands.Bot(command_prefix='>')
AVAILABLE_GAMES = {"brawler": minigames.brawler.Brawler}
currently_running_games = []


@bot.command()
async def duel(ctx, game_name: str, target: discord.Member):
    if game_name not in AVAILABLE_GAMES.keys():
        await ctx.send("You can't just type a random game name and expect it" +
                       " to work.\nAvailable games:\n    " +
                       "    \n".join(AVAILABLE_GAMES))
        return

    if target not in ctx.guild.members:
        await ctx.send(f"Who the fuck is {target.name}?")
        return

    await ctx.send(f"{ctx.author.mention} challenges {target.mention} to a " +
                   f"game of {game_name}!")

    new_game = AVAILABLE_GAMES[game_name](ctx.message.channel, [ctx.author,
                                                                target])
    await ctx.send(new_game._show_intro())
    await ctx.send(new_game._display())
    currently_running_games.append(new_game)


@duel.error
async def info_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send(f"Who the fuck is that?")
    else:
        raise error


@bot.listen()
async def on_ready():
    print("Ready.")

bot.run(token)
