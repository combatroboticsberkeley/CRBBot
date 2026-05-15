from nextcord.ext import commands, tasks

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

import datetime
from datetime import timedelta

class EventCommands(commands.Cog):
    CHECK_FOR_EVENT_INTERVAL = 60 # in secs
    MAX_CONCUR_EVENT_READS = 10
    MINUTES_EARLY_FOR_PING = 1

    def __init__(self, bot:commands.Bot, channel_id:int, calendar_id:str, service_account_file:str, permitted_roles:list[str]):
        self.bot = bot
        self.calendar_id = calendar_id
        self.pinged_events = []
        self.permitted_roles = permitted_roles
        self.channel = self.bot.get_channel(channel_id)

        SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
        credentials = Credentials.from_service_account_file(
            service_account_file, scopes=SCOPES)
        
        self.calendar_service = build('calendar', 'v3', credentials=credentials)

        self.handle_event_pings.start()

    async def ping_for_event(self, event):
        start = event['start'].get('dateTime', event['start'].get('date'))
        dt = datetime.datetime.fromisoformat(start.replace('Z', '+00:00'))
        start_formatted = dt.strftime("%b %d, %Y at %I:%M %p")

        title = event.get('summary', 'This event had no title :(')
        description = event.get('description', "This event had no description :(")

        message = f"# {title} begins at {start_formatted} \n {description}"

        await self.channel.send(message) # type: ignore

    @tasks.loop(seconds=CHECK_FOR_EVENT_INTERVAL)
    async def handle_event_pings(self, ctx:commands.Context):
        # Get current time in UTC formatted for Google API
        now_time = datetime.datetime.now(datetime.timezone.utc)
        now = now_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

        new_time = now_time + timedelta(minutes=self.MINUTES_EARLY_FOR_PING)
        shouldPingUpperbound = new_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        
        events_result = self.calendar_service.events().list(
            calendarId = self.calendar_id, 
            timeMin=now,
            timeMax=shouldPingUpperbound,
            maxResults=self.MAX_CONCUR_EVENT_READS, 
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        
        for event in events:            
            if (event not in self.pinged_events):
                self.pinged_events.append(event)
                await self.ping_for_event(event)

        # remove pinged events that are no longer occuring
        for event in self.pinged_events[:]:
            if event not in events:
                self.pinged_events.remove(event)