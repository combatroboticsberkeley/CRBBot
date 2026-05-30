from nextcord.ext import commands, tasks
import nextcord

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

import datetime
from datetime import timedelta

# from typing import TYPE_CHECKING
# if TYPE_CHECKING: # This only runs for type checkers, preventing circular errors at runtime
#     from CRBBot import CRBBot

from CalendarChannelPair import CalendarChannelPair

class EventCommands(commands.Cog):
    CHECK_FOR_EVENT_INTERVAL = 10  # in secs
    MAX_CONCUR_EVENT_READS = 30
    MINUTES_INTO_FUTURE_TO_CHECK = 2880
    MINUTES_EARLY_TO_PING = {30 : "occurs in <30 min", 1440 : "occurs in <24 hrs"} # 1440 is 60*24 minutes = a day - Cai,

    def __init__(self, bot, service_account_file: str):
        self.bot = bot
        self.pinged_events:dict = {} # stores a calendar_id : [list of pinged events] pair for each calendar_id in self.bot.calendar_channel_pairs

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

    async def ping_for_event(self, event_info, channel_id: int):
        event = event_info[1]
        start = event['start'].get('dateTime', event['start'].get('date'))
        dt = datetime.datetime.fromisoformat(start.replace('Z', '+00:00'))
        start_formatted = dt.strftime("%b %d, %Y at %I:%M %p")

        channel = self.bot.get_channel(channel_id)

        title = event.get('summary', 'This event had no title :(')
        description = event.get('description', "This event had no description :(")

        message = f"# {title} begins on {start_formatted} ({self.MINUTES_EARLY_TO_PING[event_info[0]]}) \n{self.parse_event_description(description, channel.guild)}"  # type: ignore

        # print(f"Attempted to send {message} into {channel.name}")

        await channel.send(message)  # type: ignore

    def get_date_x_minutes_before_event(self, event, x):
        start = event['start'].get('dateTime', event['start'].get('date'))
        start_date = datetime.datetime.fromisoformat(start.replace('Z', '+00:00'))
        return start_date - timedelta(minutes=x)

    def generate_event_pings(self, event):
        now_time = datetime.datetime.now(datetime.timezone.utc)
        for minutes_early_to_ping in self.MINUTES_EARLY_TO_PING:
           if now_time > self.get_date_x_minutes_before_event(event, minutes_early_to_ping):
               yield (minutes_early_to_ping, event) 
               
    def gather_pingable_events(self, events):
        for event in events:
            yield from self.generate_event_pings(event)

    async def handle_event_pings(self, calendar_channel_pair: CalendarChannelPair):
        now_time = datetime.datetime.now(datetime.timezone.utc)
        now = now_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

        new_time = now_time + timedelta(minutes=self.MINUTES_INTO_FUTURE_TO_CHECK)
        shouldPingUpperbound = new_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

        try:
            events_result = self.calendar_service.events().list(
                calendarId=calendar_channel_pair.calendar_id,
                timeMin=now,
                timeMax=shouldPingUpperbound,
                maxResults=self.MAX_CONCUR_EVENT_READS,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
        except Exception as e:
            print(f"[EventCommands] Failed to fetch events for calendar "
                f"{calendar_channel_pair.calendar_id}: {e}")
            return

        events = events_result.get('items', [])

        # print(f'{calendar_channel_pair.calendar_id} has {events} events')

        pingable_events = list(self.gather_pingable_events(events))

        for event_info in pingable_events: #type: ignore
            if event_info not in self.pinged_events.get(calendar_channel_pair.calendar_id, []):
                calendar_id_pinged_events = self.pinged_events.get(calendar_channel_pair.calendar_id, [])
                calendar_id_pinged_events.append(event_info)
                self.pinged_events[calendar_channel_pair.calendar_id] = calendar_id_pinged_events
                await self.ping_for_event(event_info, calendar_channel_pair.channel_id) #type: ignore

        for event_info in self.pinged_events.get(calendar_channel_pair.calendar_id, [])[:]:
            if event_info not in pingable_events:
                self.pinged_events[calendar_channel_pair.calendar_id].remove(event_info)

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
        self.pinged_events.get(self.bot.calendar_channel_pairs[self.bot.LEADS_CALENDAR_CHANNEL].calendar_id,[]).clear()
        await interaction.response.send_message(
            f'Successfully made the Lead Calendar Channel "{interaction.channel.name}"!', ephemeral=True  # type: ignore
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
        self.pinged_events.get(self.bot.calendar_channel_pairs[self.bot.GENERAL_CALENDAR_CHANNEL].calendar_id,[]).clear()
        await interaction.response.send_message(
            f'Successfully made the General Calendar Channel "{interaction.channel.name}"!', ephemeral=True  # type: ignore
        )
