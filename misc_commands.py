from nextcord.ext import commands
import nextcord

import asyncio

class MiscCommands(commands.Cog):
    unitWordConversions = {
        # Month abbreviations
        "mo": "month",
        "mon": "month",
        "mos": "month",
        "months": "month",
        
        # Week abbreviations
        "w": "week",
        "wk": "week",
        "wks": "week",
        "weeks": "week",
        
        # Day abbreviations
        "d": "day",
        "dy": "day",
        "days": "day",
        
        # Hour abbreviations
        "h": "hour",
        "hr": "hour",
        "hrs": "hour",
        "hours": "hour",
        
        # Minute abbreviations
        "m": "minute",
        "min": "minute",
        "mins": "minute",
        "minutes": "minute",
        
        # Second abbreviations
        "s": "second",
        "sec": "second",
        "secs": "second",
        "seconds": "second"
    }

    unitConversions = {
        "month": 4*7*24*60*60, 
        "week": 7*24*60*60, 
        "day" : 24*60*60, 
        "hour": 60*60, 
        "minute": 60, 
        "second": 1
    }

    def __init__(self, bot,  permitted_roles:list[str]):
        self.bot = bot
        self.permitted_roles = permitted_roles

    @commands.command(aliases=["rmd", "rmdthem"])
    async def remind(self, ctx:commands.Context, delay:float, units:str, *text):
        """
        Reminds all pinged people of "text" after "mins" minutes
        """

        userMentions = ", ".join([user.mention for user in ctx.message.mentions])
        text = " ".join(text)
        await ctx.reply(f'Succesfully set Reminder for {userMentions} of "{text}" for in {delay} {self.unitWordConversions[units]}(s)!')
        await asyncio.sleep(self.unitConversions[self.unitWordConversions[units]]*delay)
        await ctx.reply(f"REMINDER for {userMentions}: {text}")