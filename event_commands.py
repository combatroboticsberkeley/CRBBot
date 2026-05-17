from nextcord.ext import commands, tasks
import nextcord

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

import datetime
from datetime import timedelta

class EventCommands(commands.Cog):
    CHECK_FOR_EVENT_INTERVAL = 15  # in secs
    MAX_CONCUR_EVENT_READS = 10
    MINUTES_EARLY_FOR_PING = 1

    def __init__(self, bot, calendar_id: str, service_account_file: str, permitted_roles: list[str]):
        self.bot = bot
        self.calendar_id = calendar_id
        self.pinged_events = []
        self.permitted_roles = permitted_roles

        SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
        credentials = Credentials.from_service_account_file(
            service_account_file, scopes=SCOPES)

        self.calendar_service = build('calendar', 'v3', credentials=credentials)

        self.handle_event_pings.start()

    def contains_permitted_roles(self, roles):
        if self.permitted_roles:
            return any([role.name in self.permitted_roles for role in roles])
        return True

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

    async def ping_for_event(self, event):
        start = event['start'].get('dateTime', event['start'].get('date'))
        dt = datetime.datetime.fromisoformat(start.replace('Z', '+00:00'))
        start_formatted = dt.strftime("%b %d, %Y at %I:%M %p")

        channel = self.bot.get_channel(self.bot.meeting_channel_id)

        title = event.get('summary', 'This event had no title :(')
        description = event.get('description', "This event had no description :(")

        message = f"# {title} begins on {start_formatted} \n{self.parse_event_description(description, channel.guild)}"  # type: ignore

        await channel.send(message)  # type: ignore

    @tasks.loop(seconds=10)
    async def handle_event_pings(self):
        now_time = datetime.datetime.now(datetime.timezone.utc)
        now = now_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

        new_time = now_time + timedelta(minutes=self.MINUTES_EARLY_FOR_PING)
        shouldPingUpperbound = new_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

        events_result = self.calendar_service.events().list(
            calendarId=self.calendar_id,
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
                await self.ping_for_event(event)

        for event in self.pinged_events[:]:
            if event not in events:
                self.pinged_events.remove(event)

    @handle_event_pings.before_loop
    async def before_handle_event_pings(self):
        await self.bot.wait_until_ready()

    @nextcord.slash_command(
        name="set_meeting_channel",
        description="Sets the current channel as the channel where meeting pings are sent."
    )
    async def set_meeting_channel(self, interaction: nextcord.Interaction):
        if not self.contains_permitted_roles(interaction.user.roles):  # type: ignore
            await interaction.response.send_message(
                "You don't have permission to use this command.", ephemeral=True
            )
            return

        self.bot.meeting_channel_id = interaction.channel_id
        self.pinged_events = []
        await interaction.response.send_message(
            f'Successfully made the Meeting Channel "{interaction.channel.name}"!'  # type: ignore
        )
