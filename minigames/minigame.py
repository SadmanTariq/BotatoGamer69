# from discord import Member
from discord import TextChannel
from random import randint
from time import time


class Minigame:
    """Placeholder class for minigames"""
    channel = None
    members = []
    current_player_index = None
    winner = None
    tie = False
    timeout = 60.0  # Number of seconds after which the game will timeout.
    timeout_timestamp = 0.0  # The unix timestamp of timeout.
    debug = False

    def __init__(self, _channel: TextChannel, _players: list, debug=False):
        self.channel = _channel
        self.members = _players
        self.current_player_index = randint(0, len(_players) - 1)
        self.debug = debug

        self._update_timeout()

        self._initialise(_channel, _players)

    def _initialise(self, _channel: TextChannel, _players: list):
        pass

    def _show_intro(self):
        """Displays introduction messages. Always called once after
        initialization."""
        # current_player_mention = self.members[self.current_player_index]
        # current_player_mention = current_player_mention.mention
        # return f"Your turn, {current_player_mention}."
        intro = "FIGHT! FIGHT! FIGHT!"
        if self.debug:
            intro = "**DEBUG MODE**\n" + intro

        return intro

    def _update_timeout(self):
        """Update the timeout_timestamp."""
        self.timeout_timestamp = time() + self.timeout

    def _timeout_updates(self):
        """Optional function for doing updates after timeout."""
        pass

    def timeout_message(self) -> str:
        """Return message to be sent when timed out."""
        current_player_mention = self.members[self.current_player_index]
        current_player_mention = current_player_mention.mention
        return_string = f"Boooo. {current_player_mention} wimped out. "
        return_string += "Timeout!"

        self._timeout_updates()

        return return_string

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
