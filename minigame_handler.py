# import discord
from on_message_commands import OnMessageCommands


class MinigameHandler(OnMessageCommands):
    def exec_check(self, message):
        if message.content.lower().startswith(">duel "):
            return True
        return False

    async def respond(self, message):
        pass
