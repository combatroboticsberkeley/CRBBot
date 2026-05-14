import nextcord
from nextcord.ext import commands

from crb_commands import CRBCommands
from gemini_commands import GeminiCommands
from gemini_commands import MarkdownUICommands

# TO DO:
 # save pages into new commands using a command + markdown for page

 # delete pages using a command (have user confirm in message just sent to user?)

 # save a page into its own page text file in pages on creation
  # let saving a page overwrite existing pages

 # load all pages from their own text files in pages on start

 # get all pages using a command (give back raw markdown) (just send this to the user and let them delete it after)

 # help page (maybe make all commands self-documenting and then put on this page, make a Cog that takes an arbitrary list of Cogs as input)

 # make announcement template page and then use for pinging meetings using Google Calendar Integration

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