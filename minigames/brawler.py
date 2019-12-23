import discord
from minigames.minigame import Minigame
from random import uniform


class Brawler(Minigame):
    players = []
    _last_action = "None"
    _actions = {}

    class Player:
        """
        Player class for the brawler game.
        Attributes:
            discord_member: discord.Member object of the player.
            health: Current health.
        """
        discord_member = None
        health = 100

        def __init__(self, _member: discord.Member):
            self.discord_member = _member

    class Action:
        """
        Changes a players hp based on chance.
        Attributes:
            name: Name of the action.
            hp_change: Will be added to a player's hp.
            hit_chance: Probability of a successful hit.
            description: Will be shown as last action after a successful hit.
        """
        name = ""
        hp_change = 0
        hit_chance = 0
        description = ""

        def __init__(self, _name: str, _hp_change: int, _hit_chance: float):
            self.name = _name
            self.hp_change = _hp_change
            self.hit_chance = _hit_chance
            self.description = f"{self.name} ({self.hp_change} hp)"

    def _initialise(self, _channel: discord.TextChannel, _members: iter):
        """Called after __init__()"""
        self.players = [self.Player(member) for member in self.members]
        self._actions = {
            "1": self.Action("Heavy attack", -40, 50.0),
            "2": self.Action("Light attack", -20, 70.0),
            "3": self.Action("Heal", 20, 100.0)
        }

    def _display(self):
        """Returns a nicely formatted string to be sent."""
        def format_actions():
            string = "Available actions:\n"
            for key, action in self._actions.items():
                string += f"{key}: {action.name}\n"
            return string

        # player1_model = ""
        # player2_model = ""

        # if self.players[]
        # # @asdf's turn
        # # Last action: asdf
        # #
        # # [Name]    [Name]
        # #  O         O
        # # /|\       /|\
        # # / \       / \
        # # ❤️: 100  ❤️: 100
        # #
        # # format_actions()

        current_player_mention = self.players[self.current_player_index]
        current_player_mention = current_player_mention.discord_member.mention

        display = f"{current_player_mention}'s "
        display += "turn.\n"

        display += "`"

        display += f"Last action: {self._last_action}\n\n"

        display += f"{self.players[0].discord_member.name[:7]} "
        display += f"{self.players[1].discord_member.name[:7]}\n"
        # [Name]  [Name]

        display += " O        O     \n/|\\      /|\\    \n/ \\      / \\    \n"
        #  O        O
        # /|\      /|\
        # / \      / \

        display += f"❤️: {str(self.players[0].health).zfill(3)} "
        display += f"❤️: {str(self.players[1].health).zfill(3)} "
        # ❤️: 100  ❤️: 100

        display += "`\n"

        display += format_actions()

        return display

    def _do_action(self, action: Action):
        """Change a player's hp based on the action"""

        # Calculate hit chance.
        hit_chance = action.hit_chance
        hit = False
        if uniform(0, 1) * 100 <= hit_chance:
            hit = True

        # Find target.
        target = None
        if self.current_player_index == 1:
            target = self.players[0]
        else:
            target = self.players[1]

        # Change target's hp
        hp_change = action.hp_change
        if hit:
            if target.health + hp_change < 0:
                target.health = 0
            elif target.health + hp_change > 100:
                target.health = 100
            else:
                target.health += hp_change

            self._last_action = action.description
        else:
            self._last_action = "Miss"

        # Check winner.
        if target.health <= 0:
            self.winner = self.players[self.current_player_index]

        # Switch current player.
        if self.current_player_index == 0:
            self.current_player_index = 1
        else:
            self.current_player_index = 0

    def check_turn(self, message: str):
        """Return true if message is applicable for use as a turn."""
        if message in self._actions.keys():
            return True
        else:
            return False

    def do_turn(self, message: discord.Message):
        """Peform a turn with the message."""
        self._do_action(self._actions[message.content])
