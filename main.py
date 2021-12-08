import os
import discord
from discord.ext import commands

discord_token = os.environ['BOT_TOKEN']

intent = discord.Intents.default()
intent.members = True
client = commands.Bot(command_prefix = "-", intents=intent)

@client.event
async def on_ready():
	print("Mercury is ready")

@client.command()
async def load(ctx, extension):
	client.load_extension(f'cogs.{extension}')
	await ctx.send("{} module was enable".format(extension))

@client.command()
async def unload(ctx, extension):
	client.unload_extension(f'cogs.{extension}')
	await ctx.send("{} module was disable".format(extension))

for filename in os.listdir('./cogs'):
	if filename.endswith('.py'):
		client.load_extension(f'cogs.{filename[:-3]}')

client.run(discord_token)