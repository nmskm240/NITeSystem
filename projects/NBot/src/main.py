import discord
from configparser import ConfigParser
from logging import config, getLogger
import sqlite3
import csv
import yaml

parser = ConfigParser()
parser.read("config.ini")
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)
config.dictConfig(yaml.safe_load(open("logger_config.yaml").read()))
logger = getLogger("project")

@client.event
async def on_ready():
    logger.info("bot is active!")
    await tree.sync()

#slash commands

@tree.command(name="search", description="名簿から情報を取得")
async def who(interaction: discord.Interaction, id: int):
    logger.info(f"execute who command by {interaction.user.id}")
    await interaction.response.defer(thinking=True)
    connection = sqlite3.connect("/database/circle.db")
    cursor = connection.cursor()
    cursor.row_factory = sqlite3.Row
    try:
        cursor.execute(
            """
                select name from members where id = ?
            """, (id, ))
        await interaction.followup.send(cursor.fetchone()["name"])
    except:
        logger.error(f"notfound id = {id}")
        await interaction.followup.send("データの取得に失敗しました。")
    finally:
        connection.close()

@tree.command(name="namelist", description="名簿の更新")
async def namelist(interaction: discord.Integration, csv_file: discord.Attachment):
    logger.info(f"execute namelist command by {interaction.user.id}")
    await interaction.response.defer(thinking=True)

    try: 
        await csv_file.save(".//temp.csv")
        with open("temp.csv", "r") as file:
            reader = csv.DictReader(file)
            rows = [row for row in reader]
            if "name" not in rows[0] or \
                "student_id" not in rows[0] or \
                "discord_id" not in rows[0]:
                raise KeyError()

    except csv.Error as e:
        logger.error("unsupported file")
        await interaction.followup.send("サポートされていないファイル形式です。\nCSV形式に変換して再実行してください。", silent = True)
        return
    except KeyError as e:
        logger.error("unsupported csv file")
        await interaction.followup.send("csvファイルにname、student_id, discord_idいずれかのヘッダーが存在しません。\nヘッダーを見直して再実行してください。", silent = True)
    except:
        logger.error("unhandler error")
        await interaction.followup.send("想定外のエラーが発生しました。")
        return
    
    connection = sqlite3.connect("/database/circle.db")
    cursor = connection.cursor()
    is_success = True
    try: 
        cursor.execute("begin transaction;")
        cursor.execute(
            """
                create table if not exists members ( 
                    id integer primary key autoincrement, 
                    student_id integer unique, 
                    discord_id integer unique, 
                    name text 
                )
            """
        )
        cursor.executemany(
            """
                insert into members (
                    student_id,
                    discord_id,
                    name
                ) 
                values (?, ?, ?) 
                on conflict (student_id) 
                do update set 
                    student_id = excluded.student_id 
                on conflict (discord_id) 
                do update set 
                    discord_id = excluded.discord_id
            """
            , [(row["student_id"], row["discord_id"], row["name"]) for row in rows]
        )
    except ValueError as e:
        logger.error(f"transaction errror\n {e}")
        is_success = False
        connection.rollback()
    except:
        logger.error("unhandler error")
        is_success = False
        connection.rollback()
    else:
        connection.commit()
    finally:
        connection.close()
    
    if(is_success):
        await interaction.followup.send("データベースを更新しました。")
    else:
        await interaction.followup.send("データベースの更新に失敗しました。\n時間を置いて再度実行してください。")

client.run(parser.get("DEFAULT" ,"Token"))