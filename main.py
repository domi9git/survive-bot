from nextcord.ext import commands
import nextcord
import json
import os
from clr import getcolor
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
                else:
                    print('this user isnt in the db, adding...')
                    with open("json/db.json", "w") as file:
                        load[0].update({str(userid):{}})
                        load[0][str(userid)].update({"inv":{}})
                        load[0][str(userid)].update({"map":{}})
                        file.write(json.dumps(load, indent=4))
                        print('this user has now been added')
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
        await interaction.send('done')
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
bot.run(token)
