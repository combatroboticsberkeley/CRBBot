from nextcord.ext import commands

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import datetime

class EventCommands(commands.Cog):
    def __init__(self, calendar_id:str, service_account_file:str, permitted_roles: list[str]):
        self.calendar_id = calendar_id

        SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
        credentials = Credentials.from_service_account_file(
            service_account_file, scopes=SCOPES)
        
        self.calendar_service = build('calendar', 'v3', credentials=credentials)

        self.permitted_roles = permitted_roles

    @commands.command(name='events')
    async def get_events(self, ctx:commands.Context):
        """Fetches the next 5 upcoming events from Google Calendar."""
        # Get current time in UTC formatted for Google API
        now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        
        events_result = self.calendar_service.events().list(
            calendarId= self.calendar_id, 
            timeMin=now,
            maxResults=5, 
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])

        if not events:
            await ctx.send('No upcoming events found.')
            return

        response = "**🗓️ Upcoming Events:**\n"
        for event in events:
            # Handle both timed events and all-day events
            start = event['start'].get('dateTime', event['start'].get('date'))
            
            # Format the time nicely if it's a dateTime (not an all-day date)
            if 'T' in start:
                dt = datetime.datetime.fromisoformat(start.replace('Z', '+00:00'))
                start_formatted = dt.strftime("%b %d, %Y at %I:%M %p")
            else:
                start_formatted = f"{start} (All Day)"

            summary = event.get('summary', 'Untitled Event')
            response += f"• **{summary}** - {start_formatted}\n"
        
        await ctx.send(response)