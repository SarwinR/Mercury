import fortnitepy
import base64
import json
import os

from keep_alive import keep_alive

from replit import db

import asyncio 

from fortnitepy.ext import commands

user2verify_epic_id = ""

email = os.environ['FBOT_EMAIL_A']
password = os.environ['FBOT_PASS_A']
filename = 'device_auths_a.json'

device_auth= base64.b64decode(os.getenv('FBOT_AUTH_A'))
device_auth_json = json.loads(device_auth)

async def dispatch_bot4verification():
    while(True):
        details = db['detail']
    
        global user2verify_epic_id
        user2verify_epic_id = details['epic_id']
        
        await asyncio.sleep(1)

def get_device_auth_details():
    return device_auth_json

def store_device_auth_details(email, details):
    existing = get_device_auth_details()
    existing[email] = details

    with open(filename, 'w') as fp:
        json.dump(existing, fp)

async def clear_pending_friend_request():
    for friend_request in bot.incoming_pending_friends:
        await friend_request.decline()

device_auth_details = get_device_auth_details().get(email, {})
bot = commands.Bot(
    command_prefix='!',
    auth=fortnitepy.AdvancedAuth(
        email=email,
        password=password,
        prompt_authorization_code=True,
        prompt_code_if_invalid=True,
        delete_existing_device_auths=True,
        **device_auth_details
    )
)

@bot.event
async def event_device_auth_generate(details, email):
    store_device_auth_details(email, details)

@bot.event
async def event_ready():
    print('----------------')
    print('Bot ready as')
    print(bot.user.display_name)
    print(bot.user.id)
    print('----------------')

    await clear_pending_friend_request()
    await dispatch_bot4verification()

@bot.event
async def event_friend_request(request):
    global user2verify_epic_id
    #print(request.id)
    #print(user2verify_epic_id)

    if(str(request.id) == str(user2verify_epic_id) or str(request.display_name) == str(user2verify_epic_id)):
        details = db['detail']
        details['status'] = True
        db['detail'] = details

    await request.decline()

@bot.command()
async def hello(ctx):
    await ctx.send('Hello!')

keep_alive()
bot.run()

def set_user2verify(epic_id:str):
    global user2verify_epic_id
    user2verify_epic_id = epic_id
