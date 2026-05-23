import nextcord
from nextcord.ext import commands

from page_commands import PageCommands
from event_commands import EventCommands
from misc_commands import MiscCommands

from CalendarChannelPair import CalendarChannelPair

import os

from dotenv import load_dotenv

load_dotenv()

class CRBBot(commands.Bot):
    COMMAND_PREFIX = "!"

    DEFAULT_PERMITTED_ROLES = ["Leads"]

    SERVICE_ACCOUNT_FILE = 'credentials.json'

    LEADS_CALENDAR_CHANNEL = "leads"
    GENERAL_CALENDAR_CHANNEL = "general"

    DEFAULT_CALENDAR_CHANNEL_PAIRS = {
        LEADS_CALENDAR_CHANNEL : CalendarChannelPair("7cbcd686b423d31264c3d44533b4df1c13e9295c838984a6fe44903bc9efc623@group.calendar.google.com", 1504702630985728162),
        GENERAL_CALENDAR_CHANNEL : CalendarChannelPair("piamd5t3aboib6g98k468o4uds@group.calendar.google.com", 1504670629113364621)
    }

    def __init__(self):
        intents = nextcord.Intents.default()
        intents.message_content = True 
        super().__init__(command_prefix=CRBBot.COMMAND_PREFIX, intents=intents)

        self.calendar_channel_pairs = CRBBot.DEFAULT_CALENDAR_CHANNEL_PAIRS
        self.permitted_roles = CRBBot.DEFAULT_PERMITTED_ROLES

    def contains_permitted_roles(self, roles):
        if self.permitted_roles:
            return any([role.name in self.permitted_roles for role in roles])
        return True

    async def on_ready(self):
        print(f'Logged in successfully as {self.user} (ID: {self.user.id})') #type: ignore

crb_bot = CRBBot()
crb_bot.add_cog(PageCommands(crb_bot))
crb_bot.add_cog(EventCommands(crb_bot, crb_bot.SERVICE_ACCOUNT_FILE))
crb_bot.add_cog(MiscCommands(crb_bot))

crb_bot.run(os.getenv("BOT_TOKEN")) #type: ignore
