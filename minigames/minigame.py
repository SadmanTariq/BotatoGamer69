# from discord import Member
from discord import TextChannel
from random import randint


class Minigame:
    """Placeholder class for minigames"""
    channel = None
    members = []
    current_player_index = None
    winner = None
    tie = False

    def __init__(self, _channel: TextChannel, _players: list):
        self.channel = _channel
        self.members = _players
        self.current_player_index = randint(0, len(_players) - 1)

        self._initialise(_channel, _players)

    def _initialise(self, _channel: TextChannel, _players: list):
        pass

    def _show_intro(self):
        """Displays introduction messages. Always called once after
        initialization."""
        current_player_mention = self.members[self.current_player_index]
        current_player_mention = current_player_mention.mention
        return f"Your turn, {current_player_mention}."

    def _display(self):
        raise NotImplementedError

    def do_turn(self, argstr):
        raise NotImplementedError

    def check_turn(self, message: str) -> bool:
        raise NotImplementedError

    def winner_message(self) -> str:
        if self.tie:
            return "The game has ended in a tie!"
        else:
            winner_mention = self.winner.discord_member.mention
            return f"{winner_mention} has won! Now fuck off!"
