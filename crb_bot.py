import nextcord
from nextcord.ext import commands

from page_commands import PageCommands
from event_commands import EventCommands
from misc_commands import MiscCommands

BOT_TOKEN = "MTUwNDU1NTI1ODcxMjU1NTU0MA.GGPrAs.I_ersnCUT-3YbhLqoRkk2jbXvdBTLMgyhDfzFY"
CALENDAR_ID = 'cai_scheidler@berkeley.edu'
SERVICE_ACCOUNT_FILE = 'credentials.json'
DEFAULT_MEETING_CHANNEL_ID = 1504655705087545407
PERMMITED_ROLES = ["Leads"]

class CRBBot(commands.Bot):
    COMMAND_PREFIX = "!"

    def __init__(self, meeting_channel_id):
        intents = nextcord.Intents.default()
        intents.message_content = True 
        super().__init__(command_prefix=CRBBot.COMMAND_PREFIX, intents=intents)

        self.meeting_channel_id = meeting_channel_id

    async def on_ready(self):
        print(f'Logged in successfully as {self.user} (ID: {self.user.id})') #type: ignore

crb_bot = CRBBot(DEFAULT_MEETING_CHANNEL_ID)
crb_bot.add_cog(PageCommands(crb_bot, PERMMITED_ROLES))
crb_bot.add_cog(EventCommands(crb_bot, CALENDAR_ID, SERVICE_ACCOUNT_FILE, PERMMITED_ROLES))
crb_bot.add_cog(MiscCommands(crb_bot, PERMMITED_ROLES))

crb_bot.run(BOT_TOKEN)