import os
import discord
from discord.ext import commands
from keep_alive import keep_alive

discord_token = os.environ['BOT_TOKEN']

intent = discord.Intents.default()
intent.members = True
client = commands.Bot(command_prefix="-", intents=intent)

#test

@client.event
async def on_ready():
    print("Mercury is ready")


@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send("{} module is now enable".format(extension))


@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send("{} module is now disable".format(extension))

@client.command()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    await ctx.send("{} module has been reloaded".format(extension))


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

keep_alive()
client.run(discord_token)
