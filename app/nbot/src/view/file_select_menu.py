from logging import getLogger
from pathlib import Path

import discord
from discord import ui


class FileSelectMenu(ui.Select):
    def __init__(self, directory_path: str, regexp: str, placeholder: str = "select file", min_values: int = 1, max_values: int = 1):
        self.directory_path = directory_path
        directory = Path(directory_path)

        files = directory.glob(regexp)
        options = list(map(lambda file: discord.SelectOption(label=file.name), files))
        
        super().__init__(placeholder=placeholder, options=options, min_values=min_values, max_values=max_values)
