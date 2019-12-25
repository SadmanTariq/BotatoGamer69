import discord
from minigames.minigame import Minigame
from random import uniform
from random import randrange

# Ignore my spagghetti of a program, thank you :)


class Brawler(Minigame):
    players = [None, None]
    _last_action = "None"
    _actions = {}

    class Player:
        """
        Player class for the brawler game.
        Attributes:
            discord_member: discord.Member object of the player.
            health: Current health.
            damage_modifier: Will be multiplied to any damage taken.
            model: PlayerModel instance.
        """

        class PlayerModel:
            _LEFT_CHAR_PARTS = {
                "head": ["(°°", "[°°", "[°}", " P ", " ••"],
                "left_arm": ["/", "'", "\\", "^", "V"],
                "right_arm": ['"', "<", "-", ")"]
            }
            _RIGHT_CHAR_PARTS = {
                "head": ["°°)", "°°]", "{°]", "•• "],
                "left_arm": ['"', ">", "(", "-"],
                "right_arm": ["/", "\\", "'", "^", "V"]
            }
            _NEUTRAL_CHAR_PARTS = {
                "head": [" O ", "°_°", "'-'", "'.'", "-.-"],
                "left_arm": [],
                "right_arm": [],
                "left_leg": ["/", "[", "{", "(", "!", "]", "}", ")", "!"],
                "right_leg": ["/", "[", "{", "(", "!", "]", "}", ")", "!"],
                "body": ["|"]
            }

            body_parts = {}

            def __init__(self, side: str):
                self.body_parts = self._get_parts(side)

            def _get_parts(self, side):
                available_parts = self._get_available_parts(side)
                parts = {}

                for key, item in available_parts.items():
                    parts[key] = item[randrange(len(item))]

                return parts

            def _get_available_parts(self, side):
                parts = {}
                if side == "left":
                    for key, item in self._NEUTRAL_CHAR_PARTS.items():
                        parts[key] = item.copy()
                        parts[key] += self._LEFT_CHAR_PARTS.get(key, []).copy()
                elif side == "right":
                    for key, item in self._NEUTRAL_CHAR_PARTS.items():
                        parts[key] = item.copy()
                        right_parts = self._RIGHT_CHAR_PARTS.get(key, [])
                        parts[key] += right_parts.copy()
                return parts

            def stitch(self, right, gap=4, sep=" "):
                # Heads
                stitched = self.body_parts["head"] + " " * gap + sep
                stitched += right.body_parts["head"] + " " * gap + "\n"

                # Bodies
                torso_left = self.body_parts["left_arm"]
                torso_left += self.body_parts["body"]
                torso_left += self.body_parts["right_arm"]

                torso_right = right.body_parts["left_arm"]
                torso_right += right.body_parts["body"]
                torso_right += right.body_parts["right_arm"]

                stitched += torso_left + " " * gap + sep + torso_right
                stitched += " " * gap + "\n"

                # Legs
                legs_left = self.body_parts["left_leg"] + " "
                legs_left += self.body_parts["right_leg"]

                legs_right = right.body_parts["left_leg"] + " "
                legs_right += right.body_parts["right_leg"]

                stitched += legs_left + " " * gap + sep + legs_right
                stitched += " " * gap

                return stitched

        discord_member = None
        health = 100
        damage_modifier = 1.0
        model = None

        def __init__(self, _member: discord.Member, side: str):
            self.discord_member = _member
            self.model = self.PlayerModel(side)

    class Action:
        """
        Changes a players hp based on chance.
        Attributes:
            name: Name of the action.
            hp_change: Will be added to a player's hp.
            hit_chance: Probability of a successful hit.
            description: Will be shown as last action after a successful hit.
            damage_mod: Change target's damage_modifier to this.
            target_user: If True, target is the user instead of opponent.
            hit_chance_mod: Multiplied with hit_chance every consecutive use.
            consecutive_uses: Self explanatory.
        """

        name = ""
        hp_change = 0
        hit_chance = 0
        hit_chance_mod = 1.0
        consecutive_uses = 0
        description = ""
        damage_mod = 1.0
        target_user = False

        def __init__(self, _name, _hp_change, _hit_chance, _damage_mod=1,
                     target_user=False, hit_chance_mod=1.0):
            self.name = _name
            self.hp_change = _hp_change
            self.hit_chance = _hit_chance
            self.target_user = target_user
            self.damage_mod = _damage_mod
            self.hit_chance_mod = hit_chance_mod

            self.description = self.name
            if self.hp_change != 0:
                self.description += f" ({self.hp_change} hp)"

        def _apply_hp_change(self, target):
            hp_change = self.hp_change * target.damage_modifier

            if target.health + hp_change < 0:
                target.health = 0
            elif target.health + hp_change > 100:
                target.health = 100
            else:
                target.health += hp_change

        def reset(self):
            """Reset to default"""
            self.consecutive_uses = 0

        def hit(self, user, opponent) -> str:
            """Perform the action and return last_action message."""
            # Calculate hit chance.
            modifier = self.hit_chance_mod ** self.consecutive_uses
            modified_hit_chance = self.hit_chance * modifier

            hit = False
            if uniform(0, 1) * 100 <= modified_hit_chance:
                hit = True

            # Get target.
            target = opponent
            if self.target_user:
                target = user

            # Modify target.
            if hit:
                # Change damage_mod.
                target.damage_modifier = self.damage_mod

                # Make a description
                description = self.name
                if self.hp_change != 0:
                    description += f" ({self.hp_change}"
                    if opponent.damage_modifier != 1:
                        description += f"*{opponent.damage_modifier}"
                    description += " hp)"

                # Change health.
                self._apply_hp_change(target)

                self.consecutive_uses += 1

                if modified_hit_chance <= 10:
                    return description + " Holy shit that worked!?"
                else:
                    return description
            else:
                if modified_hit_chance <= 10:
                    return "Congratulations! You just wasted a turn!"
                else:
                    return "Miss"

    def _initialise(self, _channel: discord.TextChannel, _members: iter):
        """Called after __init__()"""
        # self.players = [self.Player(member) for member in self.members]
        self.players[0] = self.Player(self.members[0], "left")
        self.players[1] = self.Player(self.members[1], "right")

        self._actions = {
            "1": self.Action("Heavy attack", -40, 50.0),
            "2": self.Action("Light attack", -20, 70.0),
            "3": self.Action("Heal", 20, 100.0, target_user=True,
                             hit_chance_mod=0.5),
            "4": self.Action("Defend", 0, 100, 0.5, True),
            "5": self.Action("`/kill @a`", 100, 5.0)
        }

    def _display(self):
        """Returns a nicely formatted string to be sent."""

        # TODO:
        # Randomly generated character models.

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
        # # [Name] | [Name]
        # #  O        O
        # # /|\      /|\
        # # / \      / \
        # # ♥: 100 | ♥: 100
        # #
        # # format_actions()

        current_player_mention = self.players[self.current_player_index]
        current_player_mention = current_player_mention.discord_member.mention

        display = f"{current_player_mention}'s "
        display += "turn.\n"

        display += "`"

        display += f"Last action: {self._last_action}\n\n"

        display += f"{self.players[0].discord_member.name[:6]} | "
        display += f"{self.players[1].discord_member.name[:6]}\n"
        # [Name]  [Name]

        display += self.players[0].model.stitch(self.players[1].model) + "\n"
        #  O       O
        # /|\     /|\
        # / \     / \

        display += f"♥: {str(int(self.players[0].health)).zfill(3)} | "
        display += f"♥: {str(int(self.players[1].health)).zfill(3)}"
        # ♥: 100  ♥: 100

        display += "`\n"

        display += format_actions()

        return display

    def _do_action(self, action: Action):
        """Change a player's hp based on the action"""
        opponent = opponent = self.players[0]
        user = self.players[self.current_player_index]

        if self.current_player_index == 0:
            opponent = self.players[1]

        last_action = action.hit(user, opponent)
        self._last_action = last_action

        # Check winner.
        if opponent.health <= 0:
            self.winner = user

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
        self._update_timeout()
        for key, action in self._actions.items():
            if key == message.content:
                self._do_action(action)
            else:
                action.reset()
        # self._do_action(self._actions[message.content])
