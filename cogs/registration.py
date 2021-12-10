import discord
from discord.ext import commands, tasks
from discord.ui import Button, View
import asyncio
from replit import db
import database_access as firebase

list_2_send_epic_id = [] #list used to store users that have to send their epic ids
db['list_2_verify_account'] = [] #list used to store users that have to verify the account

registration_message_channel = 918466005708201984
registration_log_channel = 918411571804373002

async def send_error_message(message, channel, time):
    error_msg = await channel.send(message)
    await asyncio.sleep(time)
    await error_msg.delete()


async def dispatch_bot4registration_process(self):
    
    while (True):
        if(len(db['list_2_verify_account']) != 0):
            db['list_2_verify_account'][0]['status'] = False
            db['detail'] = db['list_2_verify_account'][0]
            invite_message=discord.Embed(title="**Send Friend Request**", description="Send a friend request to this account ` mercury-a ` using your Fortnite Account with **Epic Account ID / Display Name**: ` {} ` __**within 1 minute**__".format(db['list_2_verify_account'][0]['epic_id']), color=0xfec016)
            invite_message.set_footer(text="Made ❤ by sarwin.")
            dm_channel = self.client.get_channel(db['list_2_verify_account'][0]['dm_channel_id'])
            await dm_channel.send(embed=invite_message)
            
            count = 0
            while (db['detail']['status'] == False and count <= 60):
                count += 1
                await asyncio.sleep(1)

            log_message = ""
            details = db['detail']
            if(details['status'] == True):
                status_message=discord.Embed(title="**Successfully Linked Account**", description="These 2 accounts have been linked successfully!", color=0x37ff00)
                status_message.add_field(name="Discord ID", value=details['discord_user_id'], inline=True)
                status_message.add_field(name="Fortnite Display Name", value=details['real_display_name'], inline=True)
                status_message.add_field(name="Epic Account ID", value=details['real_epic_id'], inline=False)
                status_message.set_footer(text="Made ❤ by sarwin.")

                data = {
                    'epic_id':details['real_epic_id'],
                    'display_name':details['real_display_name']
                }
                firebase.set_link_discord2fortnite(details['discord_user_id'], data)

                user = await self.client.fetch_user(int(details['discord_user_id']))
                log_message = "{} successfully linked a fortnite account. DisplayName: `{}` Epic_ID: `{}`".format(user.mention , details['real_display_name'], details['real_epic_id'])

            else:
                status_message=discord.Embed(title="**Failed To Link Account**", description="The account linkage process failed. Below are some reasons why it might have failed. Try linking you account again. If the problem persists, contact a staff.", color=0xff0000)
                status_message.add_field(name="Did Not Invite", value="You did not send a friend request to the bot", inline=False)
                status_message.add_field(name="Wrong Fortnite Account", value="The Fortnite account you used to send the invite does not match the Epic Account ID you sent", inline=False)
                status_message.add_field(name="Incorerct Name", value="You might have mistyped your Display Name (Display Name is CaSe SenSItIvE!). If your name consists of weird characters, use your **Epic Account ID** instead", inline=False)

                user = await self.client.fetch_user(int(details['discord_user_id']))
                log_message = "{} tried to link an account with DisplayName / Epic Account ID: `{}` but failed.".format(user.mention , details['epic_id'])

            database = db['list_2_verify_account']
            database.pop(0)
            db['list_2_verify_account'] = database
            await dm_channel.send(embed=status_message)

            global registration_log_channel
            log_channel = self.client.get_channel(registration_log_channel)
            await log_channel.send(log_message)

        await asyncio.sleep(5)

async def start_registration_process(interaction):
    #check if player is already registered

    if(firebase.check_if_already_registered(interaction.user.id)):
        error_msg = "{} you are already registered!".format(interaction.user.mention)
        await send_error_message(error_msg, interaction.channel, 10)
        return

    global list_2_send_epic_id
    for entry in list_2_send_epic_id:
        if(entry['discord_user_id'] == interaction.user.id):
            error_msg = "{} you have already requested an account linkage process. Check your DMs.".format(interaction.user.mention)
            await send_error_message(error_msg, interaction.channel, 10)
            return
    for entry in db['list_2_verify_account']:
        if(entry['discord_user_id'] == interaction.user.id):
            error_msg = "{} you have already requested an account linkage process. Please wait for the bot to ask you to verify your account. Check DM.".format(interaction.user.mention)
            await send_error_message(error_msg, interaction.channel, 10)
            return
            

    user = interaction.user
    dm_channel = user.dm_channel
    if(dm_channel == None):
        dm_channel = await user.create_dm()

    entry = {
        'discord_user_id' : user.id,
        'dm_channel_id' : dm_channel.id
    }

    epic_id_info = Button(label='How To Get Epic Account ID', url="https://www.epicgames.com/help/en-US/epic-accounts-c74/general-support-c79/what-is-an-epic-account-id-and-where-can-i-find-it-a3659")

    view = View()
    view.add_item(epic_id_info)

    send_epic_id_notice_message=discord.Embed(title="**Send your Epic Account ID or Display Name**", description="Send your **Epic Account ID** or **Display Name** __within 2 minutes__. Click the link below to know how to obtain your **Epic Account ID**. \n\n **NOTE** \nDisplay Name is CaSe SenSItIvE!\n\nEnsure your **Epic Account ID** or **Display Name** is correct before sending. If you enter a wrong **Epic Account ID** or **Display Name** you will need to start the process all over again!", color=0xfec016)
    send_epic_id_notice_message.set_footer(text="Made ❤ by sarwin.")

    try:
        await dm_channel.send(embed=send_epic_id_notice_message, view=view)
        list_2_send_epic_id.append(entry)
    except:
        error_msg = "{} your DM is **inaccessible**\nUnblock the bot _or/and_ set your DM to public then try again in some time.".format(user.mention)
        await send_error_message(error_msg, interaction.channel, 10)
        return


    status = False
    count = 0
    while(status == False and count <= 60):
        if(len(list_2_send_epic_id) == 0):
            status = True
            return
        else:
            if(list_2_send_epic_id[0] != entry):
                status = True
                return
            else:
                count += 1

        await asyncio.sleep(2)
        
    timeout_message = discord.Embed(title="**Process Failed**", description="You took too long to send your **Epic Account ID**. Please restart the process.", color=0xff0000)
    timeout_message.set_footer(text="Made ❤ by sarwin.")

    try:
        await dm_channel.send(embed=timeout_message)
        list_2_send_epic_id.remove(entry)
    except:
        pass
    

class Registration(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Registration Module Ready")

        firebase.initialize_database()
        self.send_registration_message.start()
        await dispatch_bot4registration_process(self)

    @commands.Cog.listener()
    async def on_message(self, message):
        if(message.author == self.client.user):
            return

        global list_2_send_epic_id
        for entry in list_2_send_epic_id:
            if(message.channel.id == entry['dm_channel_id']):
                epic_id = message.content.strip()
                entry['epic_id'] = epic_id

                indication_message=discord.Embed(title="**Link Account**", description="These 2 accounts will be linked! You are currently number __**{}**__ in line. \n`_ETA: {} minutes(s)_` \nPlease wait for the bot to send you further instructions. Not responding to the bot will cause the process to fail!".format(len(db['list_2_verify_account']) + 1, len(db['list_2_verify_account'])), color=0xfec016)
                indication_message.add_field(name="Discord ID", value=entry['discord_user_id'], inline=True)
                indication_message.add_field(name="Epic Account ID / Display Name", value=entry['epic_id'], inline=True)
                indication_message.set_footer(text="Made ❤ by sarwin.")

                await message.channel.send(embed=indication_message)
                
                database = db['list_2_verify_account']
                database.append(entry)
                db['list_2_verify_account'] = database
                list_2_send_epic_id.remove(entry)
                return

    @tasks.loop(seconds=300)
    async def send_registration_message(self):
        register_button = Button(label='Register', style=discord.ButtonStyle.green)
        epic_id_info = Button(label='How To Get Epic Account ID', url="https://www.epicgames.com/help/en-US/epic-accounts-c74/general-support-c79/what-is-an-epic-account-id-and-where-can-i-find-it-a3659")
        tutorial_button = Button(label='Video Tutorial', url="https://discord.com/channels/803192609430044693/803582442488987688/918492757306273812")

        async def register_button_callback(interaction):
            await start_registration_process(interaction)

        register_button.callback = register_button_callback

        view = View(timeout=None)
        view.add_item(register_button)
        view.add_item(epic_id_info)
        view.add_item(tutorial_button)

        global registration_message_channel
        registration_channel = self.client.get_channel(registration_message_channel)

        await registration_channel.purge(limit=10)
        registration_message=discord.Embed(title="**Link Account**", description="Press the __Register__ button down below to begin the verification process.The bot will send instructions on how to link your account via DMs. Ensure your DM is open.\n\nNote: You will need to provide the bot with your **Epic Account ID** or **Display Name**.", color=0xfec016)
        registration_message.set_footer(text="Made ❤ by sarwin. (This is an early version. Expect errors.)")
        await registration_channel.send(embed=registration_message, view=view)

def setup(client):
    client.add_cog(Registration(client))
