import discord
from discord.ext import commands
from discord.ui import Button, View
import asyncio
from replit import db

import database_access as firebase

class Management(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Management Module Ready")

    @commands.command()
    async def unlink(self, ctx, discord_user:discord.Member):
        proceed_button = Button(label='Unlink Account?', style=discord.ButtonStyle.green)
        cancel_button = Button(label='Cancel', style=discord.ButtonStyle.danger)

        async def unlink_account_callback(interaction):
            firebase.delete_user_details(discord_user.id)
            await warning_message.delete()
            result_message = await ctx.send("Account unlinked!")
            
            await asyncio.sleep(5)
            await result_message.delete()

        async def cancel_callback(interaction):
            await warning_message.delete()

        proceed_button.callback = unlink_account_callback
        cancel_button.callback = cancel_callback

        view = View()
        view.add_item(proceed_button)
        view.add_item(cancel_button)

        msg = "Do you want to unlink any Fortnite Account related to the user?"
        warning_message = await ctx.send(msg, view=view)

    @commands.command()
    async def registration_queue(self, ctx):
        await ctx.send("Number of users queued for verification is: `{}`".format(len(db['list_2_verify_account'])))

def setup(client):
    client.add_cog(Management(client))

