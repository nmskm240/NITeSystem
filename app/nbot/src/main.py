import discord
from discord.ext import commands
from configparser import ConfigParser
from logging import config, getLogger
import yaml
import coloredlogs

from database import setting, model

parser = ConfigParser()
parser.read("config.ini")
config.dictConfig(yaml.safe_load(open("logger_config.yaml").read()))
logger = getLogger("nbot")
coloredlogs.install()

model.base.Base.metadata.create_all(bind=setting.Engine)

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned, intents=discord.Intents.all(), help_command= None)
    
    async def setup_hook(self) -> None:
        logger.info("setup hook")
        await self.load_extension("command.members")
        await self.tree.sync(guild=discord.Object(id="853968633340100648"))

    async def on_ready(self):
        await self.change_presence(activity=discord.Game(name="動作確認", type=1))
        logger.info("bot is active!")

bot = Bot()
bot.run(parser.get("DEFAULT" ,"Token"))