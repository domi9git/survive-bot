from nextcord.ext import commands
import nextcord
import requests
import json
TESTING_GUILD_ID = guild_id  # Replace with your guild ID

bot = commands.Bot()

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.slash_command(description="the hi command", guild_ids=[TESTING_GUILD_ID])
async def hi(interaction: nextcord.Interaction,
    obj: nextcord.User = nextcord.SlashOption(
        name="object",
        description="name of the object",
        required=False
        )
    ):
    await interaction.response.defer(with_message=True)
    with interaction.channel.typing():
        if not obj:
            await interaction.send(f'hello {interaction.user.mention}')
        else:
            await interaction.send(f'hello @{obj}')
bot.run(token)