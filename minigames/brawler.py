import discord
from minigames.minigame import Minigame


class Brawler(Minigame):
    players = []

    class Player:
        discord_member = None
        health = 100

        def __init__(self, _member: discord.Member):
            self.discord_member = _member

    def _initialise(self, _channel: discord.TextChannel, _members: iter):
        self.players = [self.Player(member) for member in self.members]

    def _display(self):
        # player1_model = ""
        # player2_model = ""

        # if self.players[]
        # # [Name]  [Name]
        # #  O       O
        # # /|\     /|\
        # # / \     / \
        # # H: 100  H: 100
        # #
        # # <:heart:658327454343233536>: 100 <:heart:658327454343233536>: 100
        # player1_model = " O \n/|\\\n/ \\"
        display = "`"

        display += f"{self.players[0].discord_member.name[:7]} "
        display += f"{self.players[1].discord_member.name[:7]}\n"
        # [Name]  [Name]

        display += " O        O \n/|\\      /|\\\n/ \\      / \\\n"
        #  O        O
        # /|\      /|\
        # / \      / \

        display += f"❤️: {str(self.players[0].health).zfill(3)} "
        display += f"❤️: {str(self.players[1].health).zfill(3)} "
        # ❤️: 100  ❤️: 100

        display += "`"

        return display
