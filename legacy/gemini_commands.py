import nextcord
from nextcord.ext import commands

# 1. Create a View to hold your interactive buttons
class FancyView(nextcord.ui.View):
    def __init__(self):
        # timeout=None means the buttons won't expire and stop working after a set time
        super().__init__(timeout=None)

    # Create a green button with a rocket emoji
    @nextcord.ui.button(label="Click Me!", style=nextcord.ButtonStyle.green, emoji="🚀")
    async def click_me_button(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        # Respond only to the person who clicked it (ephemeral=True)
        await interaction.response.send_message(f"Awesome! Thanks for clicking, {interaction.user.mention}!", ephemeral=True)

    # Create a red button to delete the message
    @nextcord.ui.button(label="Delete", style=nextcord.ButtonStyle.red, emoji="🗑️")
    async def delete_button(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        # Delete the message that the button is attached to
        await interaction.message.delete()

    # You can also add standard Link buttons
    # Link buttons don't need a callback function, they just open the URL
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        
# 2. Create the Cog that holds the command
class GeminiCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def fancy(self, ctx: commands.Context):
        # --- Build the Embed ---
        embed = nextcord.Embed(
            title="✨ Super Fancy Embed ✨",
            description="This is a demonstration of an embed with **interactive buttons** and rich formatting.",
            color=nextcord.Color.blurple() # You can also use a hex code like color=0x9B59B6
        )

        # Set the author to whoever ran the command, using their profile picture
        embed.set_author(name=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.display_avatar.url)
        
        # Add a cool thumbnail image to the top right
        embed.set_thumbnail(url="https://nextcord.dev/assets/logo.png") 

        # Add fields (columns/rows of text)
        embed.add_field(name="Cool Feature 1", value="Interactive Buttons!", inline=True)
        embed.add_field(name="Cool Feature 2", value="Dynamic user mentions!", inline=True)
        embed.add_field(name="Pro Tip 💡", value="You can add up to 25 fields in a single embed.", inline=False)

        # Add a footer to the bottom
        bot_avatar = self.bot.user.display_avatar.url if self.bot.user else None
        embed.set_footer(text="Powered by Nextcord UI", icon_url=bot_avatar)

        # --- Create the View ---
        view = FancyView()

        # Add a link button directly to the view instance
        view.add_item(nextcord.ui.Button(label="Nextcord Docs", style=nextcord.ButtonStyle.link, url="https://docs.nextcord.dev/"))

        # --- Send the Message ---
        # Pass both the embed and the view into the send function
        await ctx.send(embed=embed, view=view)

# (If your bot is all in one file, you would add this to your bot like this:)
# crb_bot.add_cog(FancyCommands(crb_bot))

class MarkdownUICommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def markdown(self, ctx: commands.Context):
        # We use a multi-line f-string to build the message.
        # Discord reads headers (###), blockquotes (>), bold (**), and links ([]())
        
        message_content = f"""
### ✨ Super Fancy Markdown UI ✨
> **Requested by:** {ctx.author.display_name}

This is a demonstration of a highly structured message using **Discord's Markdown** formatting instead of a formal embed.

**Cool Feature 1**
> Markdown is natively supported everywhere and doesn't require complex objects!

**Cool Feature 2**
> Dynamic user mentions work perfectly: {ctx.author.mention}

**Pro Tip 💡**
> You can fake buttons using brackets and text formatting.

---
*Powered by standard text formatting*

Actions: `[ 🚀 Click Me! ]` • `[ 🗑️ Delete ]` • [🔗 Nextcord Docs](https://docs.nextcord.dev/)
"""

        # Send the string as standard content
        await ctx.send(content=message_content)

# crb_bot.add_cog(MarkdownUICommands(crb_bot))