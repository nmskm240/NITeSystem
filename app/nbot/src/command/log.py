import logging
from pathlib import Path

import discord
from discord import app_commands, ui
from discord.ext import commands
from view.file_select_menu import FileSelectMenu

LOGS_DIRECTORY = "./logs"
LOG_FILE_EXTENTION = ".log"
LOG_FILE_REGEXP = f"*{LOG_FILE_EXTENTION}*"
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
            await interaction.response.defer(ephemeral=True)
            view = LogFileSelector()
            await interaction.followup.send(view=view, ephemeral=True)
        else:
            await interaction.followup.send(file=discord.File(Path(LOGS_DIRECTORY).joinpath(LOG_FILE_EXTENTION)), ephemeral=False)

class LogFileSelector(ui.View):
    def __init__(self, *, timeout: float | None = 180):
        super().__init__(timeout=timeout)
        
        self.selector = FileSelectMenu(directory_path=LOGS_DIRECTORY, regexp=LOG_FILE_REGEXP)
        self.add_item(self.selector)

        self.selector.callback = self.on_select

    async def on_select(self, interaction: discord.Interaction):
        logger.info("selected file")
        directory = Path(self.selector.directory_path)
        file_not_found = True

        for selected in interaction.data["values"]:
            path = directory.joinpath(selected)
            
            if path.exists():
                if file_not_found:
                    self.selector.disabled = True
                    logger.info(f"${self.selector.options}")
                    await interaction.response.edit_message(view=self)
                await interaction.followup.send(file=discord.File(path))
                file_not_found = False

        if file_not_found:
            await interaction.response.send_message("ファイルが見つかりませんでした")


async def setup(bot: commands.Bot):
    await bot.add_cog(Log(bot), guild=discord.Object(id="853968633340100648"))
