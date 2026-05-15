from nextcord.ext import commands

import asyncio

class MiscCommands(commands.Cog):
    def __init__(self, bot,  permitted_roles:list[str]):
        self.bot = bot
        self.permitted_roles = permitted_roles

    @commands.command(aliases=["rmdme"])
    async def remind_me(self, ctx:commands.Context, text:str, mins:float):
        """
        Reminds the user of "text" after "mins" minutes
        """
        await ctx.reply(f'Succesfully set Reminder "{text}" for in {mins} mins!')
        await asyncio.sleep(60*mins)
        await ctx.reply(f"REMINDER for {ctx.author.mention}: {text}")