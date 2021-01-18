# bossbadi's discord bot: resource module

import discord, traceback, random, datetime, os, asyncio

from matplotlib import pyplot as plt
from bot.embed.embed_cmds import *
from bot.web_scraping.scrape import *

recent_guilds = []
log_msgs = True

ADMIN_ID = '712323326575378562'
CANNOT_SEND_EMPTY_MSG = ":face_with_raised_eyebrow: The message cannot be empty!"
cooldown_silent = {}  # silent cooldown for every other command


def cooldown_start(content, userid):
    if content.startswith("="):  # cooldowns commands
        cooldown_silent[userid] = 0

async def cooldown_end(userid):
    await asyncio.sleep(1)
    decool_silent(userid)

def decool_silent(userid):  # remove user from silent/main cooldown
    if userid in cooldown_silent: del cooldown_silent[userid]


def check_for_ping(content, userid):
    has_ping = False
    discord_user_id = None

    if ('@everyone' in content) or ('@here' in content):  # check for mass ping
        has_ping = True
    elif ('<@' in content and '>' in content):  # check for user/role ping
        if '<@!' in content:  # check for user ping
            discord_user_id = content[content.find("<@!") + 3:content.find(">")]
            if discord_user_id != userid:  # user can ping themselves
                if discord_user_id.isdigit():  # checking if it's an ID
                    discord_user_id = int(discord_user_id)
        elif '<@&' in content:
            role_id = content[content.find("<@&") + 3:content.find(">")]
            if role_id.isdigit():  # checking if it's an ID
                has_ping = True

    return has_ping, discord_user_id



def get_devs(userid, data):
    result = None

    data = data.replace(" ", "")
    data = data.split("),(")

    for i, point in enumerate(data): data[i] = point.strip("()")

    dev_x = []
    dev_y = []

    for point in data:
        point1 = point.split(',')

        if len(point1) == 2:  # if it's an ordered pair
            try: dev_x.append(float(point1[0]))  # adding another x-value
            except: result = f':face_with_raised_eyebrow: Error in `{point1[0]}`. Invalid number?'

            try: dev_y.append(float(point1[1]))  # adding another y-value
            except: result = f':face_with_raised_eyebrow: Error in `{point1[1]}`. Invalid number?'
        else: result = f":face_with_raised_eyebrow: Error in `({point})`. This must be one ordered pair."

    if not result:
        plt.grid(True)
        plt.plot(dev_x, dev_y)

        result = f"bot/images/graph_{userid}.png"
        plt.savefig(result)
        plt.close()

    return result