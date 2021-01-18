# bossbadi's discord bot: embed commands descriptions

BOT_LOG = """```
12/24/2020
v0.0.4
    -Possible cooldown bug fixed (bot doesn't respond)
    -Error messages sent in text channel, no more DMs
```"""

# ---important stuff---#
BOT_ID = '778450224904536067'  # bot id
BOT_MENTION = f"<@!{BOT_ID}>"  # when someone mentions bot
a_talk = "Imagine a bot with all my features plus more. Well then you have [botbadi](http://gopubby.com/botbadi), the ultimate multipurpose bot with music, economy, moderation, and more."

EMBED_FOOTER = "<> parameters are required, but don't actually type <>"

DESC_MAIN = """
I am NumericBoss, a Discord bot that specializes in numbers. I can do dice rolls and coin flips. I can also calculate your math problems (which is very useful).

**Randomness**
`=flip` or `=coin` Flip a two-sided coin
`=roll` or `=dice` Roll a six-sided die
`=rand <Start> <End>` Generate a random integer

**The calculator**
`=c <Problem>` or `=calc <Problem>` Calculate a math problem (examples below)
```
=c 100! 99! 98! 97! 96!
=c sin(cos(tan(asin(acos(atan(1))))))
=calc sqrt(i^123456789)
=calc abs(log(cbrt(-1)))
```
**The grapher**
`=graph <Ordered pairs>` Graph some ordered-pairs (example below)
```=graph (0 ,2) , ( 3,4), (5, 12 )```
**Extras**
`=ping` Check bot latency
`=about` About this bot
`=fix` If the bot isn't responding (run it and it will work)
"""


BOT_INFO = """
I am a Discord bot developed using Python 3. I specialize in numbers and other random stuff. Type `=help` for my commands. You will not regret it :)

[Join my amazing support server here!](https://discord.gg/rzDqQqD)
[Invite me to your servers here!](https://discord.com/oauth2/authorize?client_id=778450224904536067&permissions=117760&scope=bot)

**Developer's message**
{}

**[Changelog](https://gist.github.com/bossbadi/57d930488cddc3182c18223a84900c3d)**
{}
"""