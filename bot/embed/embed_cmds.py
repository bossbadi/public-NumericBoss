# bossbadi's discord bot: embed commands module

from bot.embed.cmds_desc import *


def embed_help(discord):
    color = discord.Color(0).green()
    embed = discord.Embed(title="NumericBoss's commands", description=DESC_MAIN, colour=color)
    embed.set_footer(text=EMBED_FOOTER)
    return embed


def embed_about(discord, a_talk, BOT_LOG):
    color = discord.Color(0).green()
    embed = discord.Embed(title="About NumericBoss",
                          description=BOT_INFO.format(a_talk, BOT_LOG),
                          colour=color)
    return embed