import discord
from discord.ext import commands


class Essential(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        activity = discord.Game(name="Next Yunite?", type=3)
        await self.client.change_presence(status=discord.Status.idle, activity=activity)
        print("Essential Module Ready")

    @commands.Cog.listener()
    async def on_message(self, message):
        pass
        #if(message.author != self.client.user):
        #if (message.channel.id == item_shop_ch_id):
        #await send_code_promotion(message.channel)

        #await self.client.process_commands(message)

    @commands.command()
    async def ping(self, ctx):
        await ctx.send('Pong! {0} ms'.format(int(self.client.latency * 1000)))


def setup(client):
    client.add_cog(Essential(client))

