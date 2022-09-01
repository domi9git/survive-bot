from nextcord.ext import commands
import nextcord
import json
import os
from clr import getcolor
from fnd import findi
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
        userid = interaction.user.id
        if os.path.exists('json/db.json'):
            print('db json file exists')
            with open('json/db.json','r') as file:
                load = json.load(file)
                if str(userid) in load[0]:
                    print('this user is in the db')
                    item_list = findi()
                    text = ""
                    for i in item_list:
                        with open('json/items.json','r') as ifile:
                            iload = json.load(ifile)
                            text = text + iload[0][i]["name"] + "\n"
                        if i in load[0][str(userid)]["inv"]:
                            print('yes')
                            load[0][str(userid)]["inv"][i] += 1
                        else:
                            print('no')
                            load[0][str(userid)]["inv"].update({i:1})
                    with open("json/db.json", "w") as file:
                        file.write(json.dumps(load, indent=4))
                    embed = nextcord.Embed(title="You found:",description=text)
                    await interaction.send(embed=embed)
                else:
                    print('this user isnt in the db, adding...')
                    with open("json/db.json", "w") as file:
                        load[0].update({str(userid):{}})
                        load[0][str(userid)].update({"inv":{}})
                        load[0][str(userid)].update({"map":{}})
                        file.write(json.dumps(load, indent=4))
                        print('this user has now been added')
                    with open('json/db.json','r') as file:
                        load = json.load(file)
                        text = ""
                    item_list = findi()
                    for i in item_list:
                        with open('json/items.json','r') as ifile:
                            iload = json.load(ifile)
                            text = text + iload[0][i]["name"] + "\n"
                        if i in load[0][str(userid)]["inv"]:
                            print('yes')
                            load[0][str(userid)]["inv"][i] += 1
                        else:
                            print('no')
                            load[0][str(userid)]["inv"].update({i:1})
                    with open("json/db.json", "w") as file:
                        file.write(json.dumps(load, indent=4))
                    embed = nextcord.Embed(title="You found:",description=text)
                    await interaction.send(embed=embed)
        else:
            with open('json/db.json','w') as file:
                dictionary = [{
                    str(userid): {
                        "inv": {},
                        "map": {}
                    }
                }]
                file.write(json.dumps(dictionary, indent=4))
                print('db created')
            with open('json/db.json','r') as file:
                load = json.load(file)
                text = ""
            item_list = findi()
            for i in item_list:
                with open('json/items.json','r') as ifile:
                    iload = json.load(ifile)
                    text = text + iload[0][i]["name"] + "\n"
                if i in load[0][str(userid)]["inv"]:
                    print('yes')
                    load[0][str(userid)]["inv"][i] += 1
                else:
                    print('no')
                    load[0][str(userid)]["inv"].update({i:1})
            with open("json/db.json", "w") as file:
                file.write(json.dumps(load, indent=4))
            embed = nextcord.Embed(title="You found:",description=text)
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
        userid = interaction.user.id
        if os.path.exists('json/db.json'):
            print('db json file exists')
            with open('json/db.json','r') as file:
                load = json.load(file)
                if str(userid) in load[0]:
                    print('this user is in the db')
                    text = ""
                    for i in load[0][str(userid)]["inv"]:
                        with open('json/items.json','r') as ifile:
                            iload = json.load(ifile)
                            text = text + iload[0][i]["name"] + ": "
                        text = text + str(load[0][str(userid)]["inv"][i]) + "\n"
                        embed = nextcord.Embed(title="Inventory",description=text)
                    if text == "":
                        embed = nextcord.Embed(title="Inventory",description="you have nothing in your inventory")
                    await interaction.send(embed=embed)
                else:
                    print('this user isnt in the db, adding...')
                    with open("json/db.json", "w") as file:
                        load[0].update({str(userid):{}})
                        load[0][str(userid)].update({"inv":{}})
                        load[0][str(userid)].update({"map":{}})
                        file.write(json.dumps(load, indent=4))
                        print('this user has now been added')
                        text = ""
                        for i in load[0][str(userid)]["inv"]:
                            with open('json/items.json','r') as ifile:
                                iload = json.load(ifile)
                                text = text + iload[0][i]["name"] + ": "
                            text = text + str(load[0][str(userid)]["inv"][i]) + "\n"
                            embed = nextcord.Embed(title="Inventory",description=text)
                        if text == "":
                            embed = nextcord.Embed(title="Inventory",description="you have nothing in your inventory")
                        await interaction.send(embed=embed)
        else:
            with open('json/db.json','w') as file:
                dictionary = [{
                    str(userid): {
                        "inv": {},
                        "map": {}
                    }
                }]
                file.write(json.dumps(dictionary, indent=4))
                print('db created')
            with open('json/db.json','r') as file:
                text = ""
                load = json.load(file)
                for i in load[0][str(userid)]["inv"]:
                    with open('json/items.json','r') as ifile:
                        iload = json.load(ifile)
                        text = text + iload[0][i]["name"] + ": "
                    text = text + str(load[0][str(userid)]["inv"][i]) + "\n"
                    embed = nextcord.Embed(title="Inventory",description=text)
                if text == "":
                    embed = nextcord.Embed(title="Inventory",description="you have nothing in your inventory")
                await interaction.send(embed=embed)
bot.run(token)