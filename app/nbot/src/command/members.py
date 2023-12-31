import discord
from discord import app_commands
from discord.ext import commands
import logging
import csv
import pandas
from sqlalchemy.dialects import sqlite

from database.setting import create_session
import database.model as datamodel

logger = logging.getLogger("nbot.command")

@app_commands.guild_only()
class Members(commands.GroupCog, group_name="members"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):        
        if member.bot:
            return
        
        logger.info(f"remove member {member.id}")
        session = create_session()
        query = session.query(datamodel.Member).filter_by(discord_id=member.id).first()
        try:
            session.delete(query)
            session.commit()
        except:
            logger.error(f"unregisted member discord_id = {member.id}")
            session.rollback()
        finally:
            session.close()

    @app_commands.command(name="import", description="名簿をCSVからインポート")
    async def import_csv(self, interaction: discord.Interaction, csv_file: discord.Attachment):
        logger.info(f"execute members import by {interaction.user.id}")
        
        await interaction.response.defer(thinking=True)
        res, rows = await try_csv_parse(csv_file)

        if(res):
            await interaction.followup.send(res, silent=True)
            return
        
        state = sqlite.insert(datamodel.Member).values([
            dict(
                student_id = x["student_id"],
                discord_id = x["discord_id"],
                name = x["name"],
            ) for x in rows
        ])
        state = state.on_conflict_do_update(
            index_elements=["student_id", "discord_id"],
            set_=dict(
                student_id=state.excluded.student_id,
                discord_id=state.excluded.discord_id
            ),
        )
        is_complete = await try_execute_statement(state)
        if is_complete:
            res_text = "データベースを更新しました。" 
        else:
            res_text = "データベースの更新に失敗しました。\n時間を置いて再度実行してください。"
        await interaction.followup.send(res_text)

    @app_commands.command(name="export", description="名簿出力")
    async def export(self, interaction: discord.Interaction):
        logger.info(f"execute members export by {interaction.user.id}")

        await interaction.response.defer()
        session = create_session()
        query = session.query(datamodel.Member.student_id, datamodel.Member.name)
        dataframe = pandas.read_sql(str(query), session.connection(), )
        dataframe.to_csv("temp.csv")
        session.close()
        await interaction.followup.send(file=discord.File("temp.csv"))

    @app_commands.command(name="join", description="自身を名簿に登録")
    async def join(self, interaction: discord.Interaction, student_id: int, name: str):
        logger.info(f"execute members join by {interaction.user.id}")

        if 100000 > student_id or student_id >= 1000000 or not name:
            await interaction.response.send_message("入力が正しくありません。", ephemeral=True)
            return
        
        await interaction.response.defer()
        state = sqlite.insert(datamodel.Member).values([
            dict(
                student_id = student_id,
                discord_id = interaction.user.id,
                name = name,
            ) 
        ])
        state = state.on_conflict_do_update(
            index_elements=["student_id", "discord_id"],
            set_=dict(
                student_id=state.excluded.student_id,
                discord_id=state.excluded.discord_id
            ),
        )
        is_complete = await try_execute_statement(state)
        if is_complete:
            res_text = "名簿に登録しました" 
        else:
            res_text = "名簿の登録に失敗しました。\n時間を置いて再度実行してください。"
        await interaction.followup.send(res_text, ephemeral=True)

async def try_execute_statement(state: sqlite.Insert) -> bool:
    is_complet = True
    try: 
        session = create_session()
        session.execute(state)
        session.commit()
    except:
        logger.error("unhandler error")
        session.rollback()
        is_complet = False
    finally:
        session.close()
    return is_complet

async def try_csv_parse(csv_file: discord.Attachment) -> tuple[str, list[dict[str]]]:
    if not csv_file.content_type.startswith("text/csv"):
        logger.error("unsupported file")
        return "サポートされていないファイル形式です。\nCSV形式に変換して再実行してください。", []
    try: 
        await csv_file.save(".//temp.csv")
        with open("temp.csv", "r") as file:
            reader = csv.DictReader(file)
            rows = [row for row in reader]
            if "name" not in rows[0] or \
                "student_id" not in rows[0] or \
                "discord_id" not in rows[0]:
                raise KeyError()
    except KeyError as e:
        logger.error("unsupported csv file")
        return "csvファイルにname、student_id, discord_idいずれかのヘッダーが存在しません。\nヘッダーを見直して再実行してください。", []
    except:
        logger.error("unhandler error")
        return "想定外のエラーが発生しました。", []
    else:
        return "", rows

async def setup(bot: commands.Bot):
    await bot.add_cog(Members(bot), guild=discord.Object(id="853968633340100648"))
