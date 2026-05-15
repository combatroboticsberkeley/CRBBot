from nextcord.ext import commands
import nextcord

import asyncio
import re

class MiscCommands(commands.Cog):

    unitConversions = {
        "w": 7 * 24 * 60 * 60,
        "d": 24 * 60 * 60,
        "h": 60 * 60,
        "m": 60,
        "s": 1
    }

    def __init__(self, bot, permitted_roles: list[str]):
        self.bot = bot
        self.permitted_roles = permitted_roles

    def parse_delay_amount_to_secs(self, delay: str) -> int:
        total_seconds = 0
        matches = re.findall(r'(\d+)([a-zA-Z]+)', delay.lower())

        for amount, unit in matches:
            amount = int(amount)
            if unit in self.unitConversions:
                total_seconds += amount * self.unitConversions[unit]

        return total_seconds

    @nextcord.slash_command(
        name="remind",
        description="Reminds the mentioned users of a message after a delay (e.g. 1h30m, 2d, 45s)."
    )
    async def remind(
        self,
        interaction: nextcord.Interaction,
        delay: str = nextcord.SlashOption(
            name="delay",
            description="How long to wait before sending the reminder. Supports w/d/h/m/s (e.g. '1h30m', '2d', '45s').",
            required=True
        ),
        users: str = nextcord.SlashOption(
            name="users",
            description="Mention one or more users to remind (e.g. @Alice @Bob).",
            required=True
        ),
        text: str = nextcord.SlashOption(
            name="message",
            description="The reminder message to send.",
            required=True
        )
    ):
        # Re-resolve mentions from the interaction message
        mentioned_users = interaction.data.get("resolved", {}).get("users", {})  # type: ignore
        if mentioned_users:
            user_mentions = ", ".join(
                f"<@{uid}>" for uid in mentioned_users.keys()
            )
        else:
            user_mentions = users  # fallback to raw string if no resolved users

        delay_secs = self.parse_delay_amount_to_secs(delay)

        await interaction.response.send_message(
            f'Successfully set reminder for {user_mentions} — "{text}" in {delay}!'
        )
        await asyncio.sleep(delay_secs)
        await interaction.followup.send(f"REMINDER for {user_mentions}: {text}")

    @nextcord.slash_command(
        name="remindme",
        description="Reminds you of a message after a delay (e.g. 1h30m, 2d, 45s)."
    )
    async def remindme(
        self,
        interaction: nextcord.Interaction,
        delay: str = nextcord.SlashOption(
            name="delay",
            description="How long to wait before sending the reminder. Supports w/d/h/m/s (e.g. '1h30m', '2d', '45s').",
            required=True
        ),
        text: str = nextcord.SlashOption(
            name="message",
            description="The reminder message to send.",
            required=True
        )
    ):
        delay_secs = self.parse_delay_amount_to_secs(delay)
        user_mention = interaction.user.mention # type: ignore

        await interaction.response.send_message(
            f'Successfully set reminder for {user_mention} — "{text}" in {delay}!'
        )
        await asyncio.sleep(delay_secs)
        await interaction.followup.send(f"REMINDER for {user_mention}: {text}")
