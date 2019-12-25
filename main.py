import discord
from discord.ext import commands
from os import environ
import minigames.brawler
from time import time
import asyncio

VERIFIED_USERS = [340115550208262145]

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
async def duel(ctx, target: discord.Member, game_name="brawler", debug=False):
    print(ctx.message.content, ctx.message.author.mention)

    if debug:
        if ctx.author.id not in VERIFIED_USERS:
            await ctx.send("Fuck off")
            return

    game_in_current_channel = False
    for game in currently_running_games:
        if ctx.message.channel == game.channel:
            game_in_current_channel = True

    if game_in_current_channel:
        await ctx.send("Wait for the current game to end, you ADHD monkey!")
        return

    if game_name not in AVAILABLE_GAMES.keys():
        await ctx.send("You can't just type a random game name and expect it" +
                       " to work.\nAvailable games:\n    " +
                       "    \n".join(AVAILABLE_GAMES))
        return

    if target not in ctx.guild.members:
        await ctx.send(f"Who the fuck is {target.name}?")
        return

    if target == ctx.message.author:
        await ctx.send("Congratulations! You just killed yourself!")
        return

    await ctx.send(f"{ctx.author.mention} challenges {target.mention} to a " +
                   f"game of {game_name}!")

    new_game = AVAILABLE_GAMES[game_name](ctx.message.channel, [ctx.author,
                                                                target], debug)
    await ctx.send(new_game._show_intro())
    await ctx.send(new_game._display())
    currently_running_games.append(new_game)


@duel.error
async def info_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send("Who the fuck is that?")
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("`>duel <@target> [<game_name>]`")
    else:
        raise error


async def check_timeouts():
    """
    Remove games that have been timed out every check_interval seconds.
    """
    check_interval = 5  # Interval between checks in seconds.
    while True:
        current_time = time()
        for i in range(len(currently_running_games)):
            game = currently_running_games[i]
            if current_time >= game.timeout_timestamp:
                await game.channel.send(game.timeout_message())
                currently_running_games.pop(i)

        await asyncio.sleep(check_interval)


@bot.listen()
async def on_ready():
    status_message = "people fight. (>duel)"
    await bot.change_presence(activity=discord.Activity(
                      name=status_message, type=discord.ActivityType.watching))
    print("Ready.")
    await check_timeouts()


@bot.listen()
async def on_message(message: discord.Message):

    async def do_turn(game, message):
        print("Doing turn.")
        print(message.content, message.author.mention)

        game.do_turn(message)
        await message.channel.send(game._display())
        if game.winner is not None or game.tie:
            await message.channel.send(game.winner_message())
            currently_running_games.pop(i)

    for i in range(len(currently_running_games)):
        game = currently_running_games[i]
        if game.check_turn(message.content):
            if game.channel == message.channel:
                if message.author == game.members[game.current_player_index]:
                    await do_turn(game, message)
                elif game.debug:
                    await do_turn(game, message)
                else:
                    await message.channel.send(f"Not your fucking turn!")

bot.run(token)
