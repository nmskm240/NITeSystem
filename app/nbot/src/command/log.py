import discord
from discord import app_commands
from discord.ext import commands
import logging

from database.setting import create_session
import database.model as datamodel

logger = logging.getLogger("nbot.command")

@app_commands.guild_only()
class Log(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="log", description="ログファイルを表示")
    async def send_log_file(self, interaction: discord.Interaction):
        await interaction.response.send_message(file=discord.File(".log"))

async def setup(bot: commands.Bot):
    await bot.add_cog(Log(bot), guild=discord.Object(id="853968633340100648"))
