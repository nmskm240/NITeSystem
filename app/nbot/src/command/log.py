import logging
import os
from pathlib import Path

import discord
from discord import app_commands, ui
from discord.ext import commands
from view.file_select_menu import FileSelectMenu

LOGS_DIRECTORY = "./logs"
LOG_FILE_EXTENTION = ".log"
LOG_FILE_REGEXP = f"*{LOG_FILE_EXTENTION}"
FILE_SELECT_TIME_OUT = 60.0

logger = logging.getLogger("nbot.command")

@app_commands.guild_only()
class Log(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="log", description="ログファイルを表示")
    async def send_log_file(self, interaction: discord.Interaction, need_previour_file: bool):
        logger.info(f"execute log by {interaction.user.id}")
        
        if need_previour_file:
            await interaction.response.defer()
            view = ui.View(timeout=FILE_SELECT_TIME_OUT)
            selector = FileSelectMenu(directory_path=LOGS_DIRECTORY, regexp=LOG_FILE_REGEXP)
            view.add_item(selector)
            await interaction.followup.send(view=view)
        else:
            await interaction.followup.send(file=discord.File(Path(LOGS_DIRECTORY).joinpath(LOG_FILE_EXTENTION)))

async def setup(bot: commands.Bot):
    await bot.add_cog(Log(bot), guild=discord.Object(id="853968633340100648"))
