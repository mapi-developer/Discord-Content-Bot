import nextcord
from nextcord.ext import commands
import os

from cogs.keys import *

intents = nextcord.Intents.all()
allowed_mentions = nextcord.AllowedMentions(everyone = True, roles = True)

client = commands.Bot(command_prefix = "!", intents = intents, allowed_mentions=allowed_mentions)

@client.event
async def on_ready():
    print("The Bot is now ready for use!")
    print("-----------------------------")

initial_extensions = []

for filename in os.listdir("./cogs"):
    if filename.endswith("Cog.py"):
        initial_extensions.append("cogs." + filename[:-3])

if __name__ == "__main__":
    for extension in initial_extensions:
        client.load_extension(extension)

client.run(botToken)
