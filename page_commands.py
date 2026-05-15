from nextcord.ext import commands
from pathlib import Path

class PageCommands(commands.Cog):
    PAGES_DIR = "pages/"
            
    def get_existing_page_commands(self):
        return [self.generate_show_page_command(f.name) 
                for f in Path('./' + self.PAGES_DIR).iterdir() if f.is_file()]

    def __init__(self, bot:commands.Bot, permitted_roles:list[str]):
        self.bot = bot
        self.permitted_roles = permitted_roles
        
        for command in self.get_existing_page_commands():
            bot.add_command(command)

    def generate_show_page_command(self, filename: str):
        with open(self.PAGES_DIR + filename, 'r') as file:
            content = file.read()
        
        name = filename.split(".")[0]

        @commands.command(name=name)
        async def show_page_command(ctx:commands.Context):
            f"""
            {content.split("\n")}
            """
            await ctx.send(content)

        return show_page_command
    
    def contains_permitted_roles(self, roles):
        if self.permitted_roles:
            return any(role.name in self.permitted_roles for role in roles)
        return True

    @commands.command(aliases=["sp"])
    async def save_page(self, ctx:commands.Context, name:str, text:str):
        """
        Saves a page. The page can be viewed by running "!name". 
        """
        if (not self.contains_permitted_roles(ctx.author.roles)): #type: ignore
            return
        
        filename = name + ".txt"

        with open(self.PAGES_DIR + filename, "w") as file:
            file.write(text)

        self.bot.add_command(self.generate_show_page_command(filename))

        await ctx.reply(f'Succesfully saved Page "{name}"!')

    @commands.command(aliases=["dp"])
    async def del_page(self, ctx:commands.Context, name:str):
        """
        Deletes a page (if it exists).
        """
        if (not self.contains_permitted_roles(ctx.author.roles)): #type: ignore
            return
        
        filename = name + ".txt"

        Path(self.PAGES_DIR + filename).unlink(missing_ok=True)

        self.bot.remove_command(name)
        await ctx.reply(f'Succesfully deleted Page "{name}"!')

    @commands.command(aliases=["lp"])
    async def list_pages(self, ctx:commands.Context):
        """
        Lists all pages.
        """

        result: str = f'```All Pages: \n'

        for command in self.get_existing_page_commands():
            result += command.name + "\n"

        result += "```"
        
        await ctx.reply(result)