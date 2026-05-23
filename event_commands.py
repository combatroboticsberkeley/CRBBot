from nextcord.ext import commands, tasks
import nextcord

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

import datetime
from datetime import timedelta

# from typing import TYPE_CHECKING
# if TYPE_CHECKING: # This only runs for type checkers, preventing circular errors at runtim
#     from CRBBot import CRBBot

from CalendarChannelPair import CalendarChannelPair

class EventCommands(commands.Cog):
    CHECK_FOR_EVENT_INTERVAL = 10  # in secs
    MAX_CONCUR_EVENT_READS = 10
    MINUTES_EARLY_FOR_PING = 1

    def __init__(self, bot, service_account_file: str):
        self.bot = bot
        self.pinged_events = []

        SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
        credentials = Credentials.from_service_account_file(
            service_account_file, scopes=SCOPES)

        self.calendar_service = build('calendar', 'v3', credentials=credentials)

        self.event_handlers = []
        for calendar_name in self.bot.calendar_channel_pairs:
            event_handler = tasks.loop(seconds=self.CHECK_FOR_EVENT_INTERVAL)(self.handle_event_pings)
            event_handler.before_loop(self.before_handle_event_pings)
            self.event_handlers.append(event_handler)
            event_handler.start(self.bot.calendar_channel_pairs[calendar_name])

    def cog_unload(self):
        for event_handler in self.event_handlers:
            event_handler.cancel()

    def parse_event_description(self, description, guild) -> str:
        splitDescription = description.split("Roles:")
        roles = splitDescription[1].split("\n")[1:]

        roleObjects = []

        for role in roles:
            try:
                roleObject = nextcord.utils.get(guild.roles, name=role.split("@")[1])
                roleObjects.append(roleObject)
            except:
                # print(f"Role {role} not found")
                ...

        result = splitDescription[0]
        result += "Roles: \n"
        for index, roleObject in enumerate(roleObjects):
            if roleObject:
                result += f"{roleObject.mention} \n"
            else:
                result += f"{roles[index]} (Couldn't find role) \n"

        return result

    async def ping_for_event(self, event, channel_id: int):
        start = event['start'].get('dateTime', event['start'].get('date'))
        dt = datetime.datetime.fromisoformat(start.replace('Z', '+00:00'))
        start_formatted = dt.strftime("%b %d, %Y at %I:%M %p")

        channel = self.bot.get_channel(channel_id)

        title = event.get('summary', 'This event had no title :(')
        description = event.get('description', "This event had no description :(")

        message = f"# {title} begins on {start_formatted} \n{self.parse_event_description(description, channel.guild)}"  # type: ignore

        await channel.send(message)  # type: ignore

    async def handle_event_pings(self, calendar_channel_pair: CalendarChannelPair):
        now_time = datetime.datetime.now(datetime.timezone.utc)
        now = now_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

        new_time = now_time + timedelta(minutes=self.MINUTES_EARLY_FOR_PING)
        shouldPingUpperbound = new_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

        events_result = self.calendar_service.events().list(
            calendarId=calendar_channel_pair.calendar_id,
            timeMin=now,
            timeMax=shouldPingUpperbound,
            maxResults=self.MAX_CONCUR_EVENT_READS,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = events_result.get('items', [])

        for event in events:
            if event not in self.pinged_events:
                self.pinged_events.append(event)
                await self.ping_for_event(event, calendar_channel_pair.channel_id)

        for event in self.pinged_events[:]:
            if event not in events:
                self.pinged_events.remove(event)

    async def before_handle_event_pings(self):
        await self.bot.wait_until_ready()

    @nextcord.slash_command(
        name="set_lead_calendar_channel",
        description="Sets the current channel as the channel where Lead Calendar pings are sent."
    )
    async def set_lead_calendar_channel(self, interaction: nextcord.Interaction):
        if not self.bot.contains_permitted_roles(interaction.user.roles):  # type: ignore
            await interaction.response.send_message(
                "You don't have permission to use this command.", ephemeral=True
            )
            return

        self.bot.calendar_channel_pairs[self.bot.LEADS_CALENDAR_CHANNEL].channel_id = interaction.channel_id # type: ignore
        self.pinged_events = []
        await interaction.response.send_message(
            f'Successfully made the Lead Calendar Channel "{interaction.channel.name}"!'  # type: ignore
        )

    @nextcord.slash_command(
        name="set_general_calendar_channel",
        description="Sets the current channel as the channel where General Calendar pings are sent."
    )
    async def set_general_calendar_channel(self, interaction: nextcord.Interaction):
        if not self.bot.contains_permitted_roles(interaction.user.roles):  # type: ignore
            await interaction.response.send_message(
                "You don't have permission to use this command.", ephemeral=True
            )
            return

        self.bot.calendar_channel_pairs[self.bot.GENERAL_CALENDAR_CHANNEL].channel_id = interaction.channel_id # type: ignore
        self.pinged_events = []
        await interaction.response.send_message(
            f'Successfully made the General Calendar Channel "{interaction.channel.name}"!'  # type: ignore
        )
