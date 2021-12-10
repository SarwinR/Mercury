import os
os.system("pip install -U git+https://github.com/Rapptz/discord.py")
import multiprocessing

for bot in ('discord_bot', 'fortnite_bot.bot_a'):
    process = multiprocessing.Process(target=lambda: __import__(bot))
    process.start()
