import os, datetime
from dotenv import load_dotenv
import discord
from discord.ext import tasks

load_dotenv()

BOT_TOKEN = os.environ.get('BOT_TOKEN')
TARGET_CHANNEL_ID = int(os.environ.get('TARGET_CHANNEL_ID'))

client = discord.Client()

@client.event
async def on_ready():
    print(client.user.name + ' is ready.')

# Reply
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    if message.content == '/today':
        now = datetime.datetime.now()
        await message.channel.send(now.strftime("%Y/%m/%d"))

# Scheduler
@tasks.loop(minutes=1)
async def mokumoku_reminder():
    channel = client.get_channel(TARGET_CHANNEL_ID)
    now = datetime.datetime.now()
    year, week, weekday = now.isocalendar()
    hhmm = now.strftime('%H:%M')

    # 奇数週はお休み
    if week % 2 == 1:
        return

    message = ""
    if weekday == 5 and hhmm == '20:00':
        message = "明日もくもく会ですよー"
    elif weekday == 6 and hhmm == '13:00':
        message = "もくもく会はじめるよー"

    if message != "":
        await channel.send(message)


@mokumoku_reminder.before_loop
async def before():
    await client.wait_until_ready()
    print("Ready to loop")

mokumoku_reminder.start()

# Start Bot
if __name__ == "__main__":
    client.run(BOT_TOKEN)
