from nextcord.ext import commands
import nextcord
from pathlib import Path

# from typing import TYPE_CHECKING
# if TYPE_CHECKING: # This only runs for type checkers, preventing circular errors at runtim
#     from CRBBot import CRBBot

class PageCommands(commands.Cog):
    PAGES_DIR = "pages/"

    def get_existing_page_names(self) -> list[str]:
        return [f.stem for f in Path('./' + self.PAGES_DIR).iterdir() if f.is_file()]

    def __init__(self, bot):
        self.bot = bot

    def read_page(self, name: str) -> str | None:
        """Returns the content of a page file, or None if it doesn't exist."""
        filepath = Path(self.PAGES_DIR + name + ".txt")
        if not filepath.exists():
            return None
        return filepath.read_text()

    @nextcord.slash_command(
        name="view_page",
        description="View a saved page by name."
    )
    async def view_page(
        self,
        interaction: nextcord.Interaction,
        name: str = nextcord.SlashOption(
            name="name",
            description="The name of the page you want to view.",
            required=True
        )
    ):
        content = self.read_page(name)
        if content is None:
            await interaction.response.send_message(
                f'Page "{name}" does not exist.', ephemeral=True
            )
            return
        await interaction.response.send_message(content)

    @nextcord.slash_command(
        name="save_page",
        description="Save a page that can later be displayed with /page. Requires permitted role."
    )
    async def save_page(
        self,
        interaction: nextcord.Interaction,
        name: str = nextcord.SlashOption(
            name="name",
            description="The name to save the page under. Use /page <name> to display it later.",
            required=True
        ),
        text: str = nextcord.SlashOption(
            name="text",
            description="The content of the page.",
            required=True
        )
    ):
        if not self.bot.contains_permitted_roles(interaction.user.roles):  # type: ignore
            await interaction.response.send_message(
                "You don't have permission to use this command.", ephemeral=True
            )
            return

        filename = name + ".txt"
        Path(self.PAGES_DIR + filename).write_text(text)

        await interaction.response.send_message(f'Successfully saved page "{name}"!', ephemeral=True)

    @nextcord.slash_command(
        name="del_page",
        description="Delete a saved page by name. Requires permitted role."
    )
    async def del_page(
        self,
        interaction: nextcord.Interaction,
        name: str = nextcord.SlashOption(
            name="name",
            description="The name of the page to delete.",
            required=True
        )
    ):
        if not self.bot.contains_permitted_roles(interaction.user.roles):  # type: ignore
            await interaction.response.send_message(
                "You don't have permission to use this command.", ephemeral=True
            )
            return

        filepath = Path(self.PAGES_DIR + name + ".txt")
        if not filepath.exists():
            await interaction.response.send_message(
                f'Page "{name}" does not exist.', ephemeral=True
            )
            return

        filepath.unlink()
        await interaction.response.send_message(f'Successfully deleted page "{name}"!', ephemeral=True)

    @nextcord.slash_command(
        name="list_pages",
        description="List the names of all saved pages."
    )
    async def list_pages(self, interaction: nextcord.Interaction):
        names = self.get_existing_page_names()

        if not names:
            await interaction.response.send_message("No pages have been saved yet.", ephemeral=True)
            return

        result = "All Pages:\n" + "\n".join(names) + "\n"
        await interaction.response.send_message(result, ephemeral=True)
