import discord
from discord import app_commands
from discord.ext import commands
import logging
import sqlite3
import csv

logger = logging.getLogger("project")

@app_commands.guild_only()
class Members(commands.GroupCog, group_name="members"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="import", description="名簿をCSVからインポート")
    async def import_csv(self, interaction: discord.Interaction, csv_file: discord.Attachment):
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
    

    @app_commands.command(name="remove", description="削除")
    async def remove(self, interaction: discord.Interaction):
        await interaction.response.send_message("remove!")

    @app_commands.command(name="export", description="名簿出力")
    async def export(self, interaction: discord.Interaction):
        await interaction.response.send_message("export")

async def setup(bot: commands.Bot):
    await bot.add_cog(Members(bot), guild=discord.Object(id="853968633340100648"))
