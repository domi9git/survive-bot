from nextcord.ext import commands
import nextcord
import json
import os
from clr import getcolor
from fnd import findi
import sqlite3
from sqlite3 import Error
TESTING_GUILD_ID = guild_id  # Replace with your guild ID

bot = commands.Bot()

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.slash_command(description="find stuff in the surrounding area", guild_ids=[TESTING_GUILD_ID])
async def find(interaction: nextcord.Interaction,
    ):
    await interaction.response.defer(with_message=True)
    with interaction.channel.typing():
        userid = int(interaction.user.id)
        conn = None
        try:
            conn = sqlite3.connect('db/main.db')
            cur = conn.cursor()
            print(sqlite3.version)
            print('connected')
            tableu = """ CREATE TABLE IF NOT EXISTS users (
                userid TEXT UNIQUE ON CONFLICT IGNORE
                ); """
            tableinv = """ CREATE TABLE IF NOT EXISTS inv (
                itemid TEXT,
                count INT,
                owner TEXT
                ); """
            cur.execute(tableu)
            print("users table is created")
            cur.execute(tableinv)
            print("inv table is created")
            cur.execute("""SELECT userid
                            FROM users
                            WHERE userid=?;""",
                            (str(userid), ))
            result = cur.fetchone()
            if result:
                print('userid already exists')
                items = findi()
                print(items)
                txt = ""
                for i in items:
                    txt = txt + i + "\n"
                    cur.execute("""SELECT itemid, owner
                                    FROM inv
                                    WHERE itemid=? AND owner=?;""",
                                    (i,str(userid)))
                    result = cur.fetchone()
                    if result:
                        cur.execute("""UPDATE inv
                                        SET count = count + 1
                                        WHERE itemid=? AND owner=?;""",
                                        (i,str(userid)))
                    else:
                        cur.execute("INSERT INTO inv(itemid,count,owner) values(?,?,?);", (i,1,str(userid)))
                embed=nextcord.Embed(title="You found:",description=txt)
            else:
                cur.execute("INSERT INTO users(userid) values(?);", (str(userid), ))
                print('inserted')
                items = findi()
                print(items)
                txt = ""
                for i in items:
                    txt = txt + i + "\n"
                    cur.execute("""SELECT itemid, owner
                                    FROM inv
                                    WHERE itemid=? AND owner=?;""",
                                    (i,str(userid)))
                    result = cur.fetchone()
                    if result:
                        cur.execute("""UPDATE inv
                                        SET count = count + 1
                                        WHERE itemid=? AND owner=?;""",
                                        (i,str(userid)))
                    else:
                        cur.execute("INSERT INTO inv(itemid,count,owner) values(?,?,?);", (i,1,str(userid)))
                embed=nextcord.Embed(title="You found:",description=txt)
            conn.commit()
        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()
                print('disconnected')
        await interaction.send(embed=embed)
@bot.slash_command(description="get item info", guild_ids=[TESTING_GUILD_ID])
async def item(interaction: nextcord.Interaction,
    id: str = nextcord.SlashOption(
        name="id",
        description="id of the item (example: stick)",
        required=True
        )
    ):
    await interaction.response.defer(with_message=True)
    with interaction.channel.typing():
        with open('json/items.json','r') as file:
            load = json.load(file)
            if str(id) in load[0]:
                embed = nextcord.Embed(title=load[0][str(id)]["name"],description=load[0][str(id)]["desc"],color=getcolor(load,id))
                await interaction.send(embed=embed)
            else:
                await interaction.send('no such item exists')
@bot.slash_command(description="checks your inventory", guild_ids=[TESTING_GUILD_ID])
async def inv(interaction: nextcord.Interaction,
    ):
    await interaction.response.defer(with_message=True)
    with interaction.channel.typing():
        userid = int(interaction.user.id)
        conn = None
        try:
            conn = sqlite3.connect('db/main.db')
            cur = conn.cursor()
            print(sqlite3.version)
            print('connected')
            tableu = """ CREATE TABLE IF NOT EXISTS users (
                userid TEXT UNIQUE ON CONFLICT IGNORE
                ); """
            tableinv = """ CREATE TABLE IF NOT EXISTS inv (
                itemid INT,
                count INT,
                owner TEXT
                ); """
            cur.execute(tableu)
            print("users table is created")
            cur.execute(tableinv)
            print("inv table is created")
            cur.execute("""SELECT userid
                            FROM users
                            WHERE userid=?""",
                            (str(userid), ))
            result = cur.fetchone()
            if result:
                print('userid already exists')
                cur.execute("""SELECT *
                                FROM inv
                                WHERE owner=?;""",
                                (str(userid), ))
                items = cur.fetchall()
                txt = ""
                for i in items:
                    txt = txt + i[0] + ": " + str(i[1]) + "\n"
                if txt == "":
                    embed=nextcord.Embed(title="Inventory",description="you have nothing in your inventory")
                else:
                    embed=nextcord.Embed(title="Inventory",description=txt)
            else:
                cur.execute("INSERT INTO users(userid) values(?)", (str(userid), ))
                print('inserted')
                cur.execute("""SELECT *
                                FROM inv
                                WHERE owner=?;""",
                                (str(userid), ))
                items = cur.fetchall()
                txt = ""
                for i in items:
                    txt = txt + i[0] + ": " + str(i[1]) + "\n"
                if txt == "":
                    embed=nextcord.Embed(title="Inventory",description="you have nothing in your inventory")
                else:
                    embed=nextcord.Embed(title="Inventory",description=txt)
            conn.commit()
        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()
                print('disconnected')
        await interaction.send(embed=embed)
bot.run(token)
