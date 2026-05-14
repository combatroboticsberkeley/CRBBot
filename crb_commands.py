from nextcord.ext import commands

class CRBCommands(commands.Cog):
    PAGES_DIR = "pages/"

    def __init__(self, bot):
        self.bot = bot
        self.load_existing_pages()
        
    def page_command_generator(self, filename):
        with open(CRBCommands.PAGES_DIR + filename, 'r') as file:
            content = file.read()
        
        @commands.command(name=filename.split(".")[0])
        async def page_command(self, ctx: commands.Context):
            await ctx.send(content)

        self.__cog_commands__ = tuple([command for command in list(self.__cog_commands__) + [page_command]]) #type: ignore

    def load_existing_pages(self):
        self.page_command_generator("helpful_links.txt")

    @commands.command()
    async def custom_command(self, ctx: commands.Context):
        await ctx.send(f'Hi {ctx.author.display_name}!')

    @commands.command()
    async def debug(self, ctx: commands.Context):
        print(self.__dict__)