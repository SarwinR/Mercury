import discord
from discord.ext import commands

welcome_channel_id = 803192609430044696

class Essential(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Welcomer Module Ready")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        message = "Welcome to the server {}. Enjoy your stay!".format(member.mention)

        global welcome_channel_id
        welcome_channel = self.client.get_channel(welcome_channel_id)
        await welcome_channel.send(message)

def setup(client):
    client.add_cog(Essential(client))