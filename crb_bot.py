import nextcord
from nextcord.ext import commands

from crb_commands import CRBCommands
from gemini_commands import GeminiCommands
from gemini_commands import MarkdownUICommands


BOT_TOKEN = "MTUwNDU1NTI1ODcxMjU1NTU0MA.GGPrAs.I_ersnCUT-3YbhLqoRkk2jbXvdBTLMgyhDfzFY"

class CRBBot(commands.Bot):
    COMMAND_PREFIX = "!"

    def __init__(self):
        intents = nextcord.Intents.default()
        intents.message_content = True 
        super().__init__(command_prefix=CRBBot.COMMAND_PREFIX, intents=intents)

    async def on_ready(self):
        print(f'Logged in successfully as {self.user} (ID: {self.user.id})')

crb_bot = CRBBot()
crb_bot.add_cog(CRBCommands(crb_bot))
# crb_bot.add_cog(GeminiCommands(crb_bot))
# crb_bot.add_cog(MarkdownUICommands(crb_bot))

crb_bot.run(BOT_TOKEN)