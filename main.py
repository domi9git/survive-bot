from nextcord.ext import commands
import nextcord
import json
import os
from clr import getcolor
from fnd import findi
from map import getloc
import sqlite3
from sqlite3 import Error
from PIL import Image
TESTING_GUILD_ID = guild_id  # Replace with your guild ID

bot = commands.Bot()

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.slash_command(description="find stuff in the surrounding area")#, guild_ids=[TESTING_GUILD_ID])
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
                userid TEXT UNIQUE ON CONFLICT IGNORE,
                map_x INT,
                map_y INT,
                biome TEXT
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
            else:
                cur.execute("INSERT INTO users(userid,map_x,map_y,biome) values(?,?,?,?);", (str(userid), 8, 4, "plains"))
                print('inserted')
            cur.execute("""SELECT map_x, map_y
                            FROM users
                            WHERE userid=?;""",
                            (str(userid), ))
            result = cur.fetchall()
            if result:
                im = Image.open(r"map/map.png")
                im = im.convert('RGBA')
                px = im.load()
                color = im.getpixel((result[0][0],result[0][1]))
                if result[0][0] < 0 or result[0][0] > im.size[0] or result[0][1] < 0 or result[0][1] > im.size[1]:
                    cur.execute("""UPDATE users
                                    SET biome = "void"
                                    WHERE userid=?;""",
                                    (str(userid), ))
                else:
                    if color == (0,255,33,255):
                        cur.execute("""UPDATE users
                                        SET biome = "plains"
                                        WHERE userid=?;""",
                                        (str(userid), ))
                    elif color == (0,38,255,255):
                        cur.execute("""UPDATE users
                                        SET biome = "river"
                                        WHERE userid=?;""",
                                        (str(userid), ))
                    elif color == (0,127,14,255):
                        cur.execute("""UPDATE users
                                        SET biome = "forest"
                                        WHERE userid=?;""",
                                        (str(userid), ))
                    elif color == (255,216,0,255):
                        cur.execute("""UPDATE users
                                        SET biome = "desert"
                                        WHERE userid=?;""",
                                        (str(userid), ))
            cur.execute("""SELECT biome
                            FROM users
                            WHERE userid=?;""",
                            (str(userid), ))
            result = cur.fetchone()
            items = findi(result)
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
                userid TEXT UNIQUE ON CONFLICT IGNORE,
                map_x INT,
                map_y INT,
                biome TEXT
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
            else:
                cur.execute("INSERT INTO inv(itemid,count,owner) values(?,?,?);", (i,1,str(userid)))
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
@bot.slash_command(description="shows where you are in the map", guild_ids=[TESTING_GUILD_ID])
async def map(interaction: nextcord.Interaction,
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
                userid TEXT UNIQUE ON CONFLICT IGNORE,
                map_x INT,
                map_y INT,
                biome TEXT
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
            else:
                cur.execute("INSERT INTO users(userid,map_x,map_y,biome) values(?,?,?,?);", (str(userid), 8, 4, "plains"))
                print('inserted')
            cur.execute("""SELECT map_x, map_y
                            FROM users
                            WHERE userid=?;""",
                            (str(userid), ))
            result = cur.fetchone()
            if result:
                px_list = getloc(result[0],result[1])
                txt = ""
                newline = 0
                for n in px_list:
                    if n == "plains":
                        txt = txt + ":green_square:"
                        newline += 1
                    if n == "river":
                        txt = txt + ":blue_square:"
                        newline += 1
                    if n == "forest":
                        txt = txt + ":deciduous_tree:"
                        newline += 1
                    if n == "desert":
                        txt = txt + ":yellow_square:"
                        newline += 1
                    if n == "void":
                        txt = txt + ":black_large_square:"
                        newline += 1
                    if newline == 5:
                        txt = txt + "\n"
                        newline = 0
                embed=nextcord.Embed(title="Map",description=txt)
            conn.commit()
        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()
                print('disconnected')
        await interaction.send(embed=embed)
@bot.slash_command(description="move in the direction you specify", guild_ids=[TESTING_GUILD_ID])
async def move(interaction: nextcord.Interaction,
    direction: str = nextcord.SlashOption(
        name="direction",
        description="the direction you want to move (examples: north, left)",
        required=True
        )
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
                userid TEXT UNIQUE ON CONFLICT IGNORE,
                map_x INT,
                map_y INT,
                biome TEXT
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
            else:
                cur.execute("INSERT INTO users(userid,map_x,map_y,biome) values(?,?,?,?);", (str(userid), 8, 4, "plains"))
                print('inserted')
            if direction == "north" or direction == "up":
                cur.execute("""UPDATE users
                                SET map_y = map_y - 1
                                WHERE userid = ?;""",
                                (str(userid), ))
            elif direction == "south" or direction == "down":
                cur.execute("""UPDATE users
                                SET map_y = map_y + 1
                                WHERE userid = ?;""",
                                (str(userid), ))
            elif direction == "east" or direction == "right":
                cur.execute("""UPDATE users
                                SET map_x = map_x + 1
                                WHERE userid = ?;""",
                                (str(userid), ))
            elif direction == "west" or direction == "left":
                cur.execute("""UPDATE users
                                SET map_x = map_x - 1
                                WHERE userid = ?;""",
                                (str(userid), ))
            cur.execute("""SELECT map_x, map_y
                            FROM users
                            WHERE userid=?;""",
                            (str(userid), ))
            result = cur.fetchone()
            if result:
                px_list = getloc(result[0],result[1])
                txt = ""
                newline = 0
                for n in px_list:
                    if n == "plains":
                        txt = txt + ":green_square:"
                        newline += 1
                    if n == "river":
                        txt = txt + ":blue_square:"
                        newline += 1
                    if n == "forest":
                        txt = txt + ":deciduous_tree:"
                        newline += 1
                    if n == "desert":
                        txt = txt + ":yellow_square:"
                        newline += 1
                    if n == "void":
                        txt = txt + ":black_large_square:"
                        newline += 1
                    if newline == 5:
                        txt = txt + "\n"
                        newline = 0
                embed=nextcord.Embed(title="Map",description=txt)
            conn.commit()
        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()
                print('disconnected')
        await interaction.send(embed=embed)
bot.run(token)
