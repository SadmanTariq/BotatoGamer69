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
async def duel(ctx, target: discord.Member, game_name="brawler"):
    # TODO:
    # Implement channel checks and timeouts

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
        await ctx.send("Who the fuck is that?")
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("`>duel <@target> [<game_name>]`")
    else:
        raise error


@bot.listen()
async def on_ready():
    print("Ready.")


@bot.listen()
async def on_message(message: discord.Message):
    for i in range(len(currently_running_games)):
        game = currently_running_games[i]
        if game.check_turn(message.content):
            if game.channel == message.channel:
                if message.author == game.members[game.current_player_index]:
                    # if True:
                    game.do_turn(message)
                    await message.channel.send(game._display())
                    if game.winner is not None or game.tie:
                        await message.channel.send(game.winner_message())
                        currently_running_games.pop(i)
                    break

bot.run(token)
