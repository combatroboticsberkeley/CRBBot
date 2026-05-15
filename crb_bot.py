import nextcord
from nextcord.ext import commands

from page_commands import PageCommands
from event_commands import EventCommands
from misc_commands import MiscCommands

# TO DO:

 # make announcement template page and then use for pinging meetings using Google Calendar Integration

BOT_TOKEN = "MTUwNDU1NTI1ODcxMjU1NTU0MA.GGPrAs.I_ersnCUT-3YbhLqoRkk2jbXvdBTLMgyhDfzFY"
CALENDAR_ID = 'cai_scheidler@berkeley.edu'
SERVICE_ACCOUNT_FILE = 'credentials.json'
MEETING_CHANNEL_ID = 1504564935261421628

class CRBBot(commands.Bot):
    COMMAND_PREFIX = "!"

    def __init__(self):
        intents = nextcord.Intents.default()
        intents.message_content = True 
        super().__init__(command_prefix=CRBBot.COMMAND_PREFIX, intents=intents)

    async def on_ready(self):
        print(f'Logged in successfully as {self.user} (ID: {self.user.id})') #type: ignore

crb_bot = CRBBot()
crb_bot.add_cog(PageCommands(crb_bot, []))
crb_bot.add_cog(EventCommands(crb_bot, MEETING_CHANNEL_ID, CALENDAR_ID, SERVICE_ACCOUNT_FILE, []))
crb_bot.add_cog(MiscCommands(crb_bot, []))

crb_bot.run(BOT_TOKEN)