from logging import getLogger
from pathlib import Path

import discord
from discord import ui

logger = getLogger("nbot.view.select_menu")


class FileSelectMenu(ui.Select):
    def __init__(self, directory_path: str, regexp: str, placeholder: str = "select file", min_values: int = 1, max_values: int = 1):
        self.directory_path = directory_path
        directory = Path(directory_path)

        files = directory.glob(regexp)
        options = map(lambda file: discord.SelectOption(label=file.name), files)
        
        super().__init__(placeholder=placeholder, options=options, min_values=min_values, max_values=max_values)

    async def callback(self, interaction: discord.Interaction):
        logger.info("selected file")
        directory = Path(self.directory_path)
        file_not_found = True

        for selected in interaction.data["values"]:
            path = directory.joinpath(selected)
            
            if path.exists():
                await interaction.response.send_message(file=discord.File(path))
                file_not_found = False

        if file_not_found:
            await interaction.response.send_message("ファイルが見つかりませんでした")
