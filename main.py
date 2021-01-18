# bossbadi's discord bot: main (executable script)
from bot.resources import *

# replit, comment and vice versa
from startup.startup_replit import *

# heroku, put token below



client = discord.Client()


# ---when bot starts---#
@client.event
async def on_ready():
    # set bot's status
    game = discord.Game(f"=help | {len(client.guilds)} servers")
    await client.change_presence(activity=game)


@client.event
async def on_guild_join(guild):
    # set bot's status
    game = discord.Game(f"=help | {len(client.guilds)} servers")
    await client.change_presence(activity=game)

    current_time = datetime.datetime.utcnow() - datetime.timedelta(hours=5)
    current_time = current_time.strftime("%b %d, %Y %I:%M %p")

    tup = 'JOIN', guild.id, guild.name, guild.member_count, current_time
    recent_guilds.append(tup)


@client.event
async def on_guild_remove(guild):
    # set bot's status
    game = discord.Game(f"=help | {len(client.guilds)} servers")
    await client.change_presence(activity=game)

    current_time = datetime.datetime.utcnow() - datetime.timedelta(hours=5)
    current_time = current_time.strftime("%b %d, %Y %I:%M %p")

    tup = 'LEAVE', guild.id, guild.name, guild.member_count, current_time
    recent_guilds.append(tup)


# ---when someone sends a message---#
@client.event
async def on_message(message):
    try:
        if type(message.channel) != discord.TextChannel:
            return

        global a_talk, log_msgs, recent_guilds

        author = str(message.author)
        channel = str(message.channel)
        server_name = str(message.guild.name)
        raw_content = str(message.content)  # will be stripped of spaces
        userid = str(message.author.id)

        if log_msgs:
            row = ['SER: ' + server_name, 'CH: ' + channel, author, raw_content]
            print(row)
            with open('log.txt', 'ab') as f:
                try:
                    f.write(f"{row}\n".encode())
                except:
                    pass

        # ---manage bots---#
        if message.author.bot:  # author cannot be bot
            return

        if raw_content.startswith(BOT_MENTION):  # bot responds to mentions as well
            raw_content = raw_content.replace(BOT_MENTION, "").strip()
            raw_content = f"={raw_content}"

        content = raw_content.replace(" ", "").replace("\n", "").lower()  # remove all spaces in content
        command = raw_content.lower()  # this is the thing that calls commands


        if command.startswith('=fix'):  # cooldown error fix
            decool_silent(userid)

        # everything silent cooldown init
        if userid in cooldown_silent: return
        cooldown_start(content, userid)

        # ---(bossbadi) change developer's message---#
        if command.startswith('=a.change'):
            if userid == ADMIN_ID:
                a_talk = raw_content[9:].strip()
                if a_talk:
                    await message.channel.send("The developer's message has been changed.")
                else:
                    await message.channel.send(CANNOT_SEND_EMPTY_MSG)

        # ---(bossbadi) reset developer's message---#
        elif command.startswith('=a.reset'):
            if userid == ADMIN_ID:
                a_talk = "This is where important information the developer has will go. You're welcome."
                await message.channel.send("The developer's message has been reset.")

        # ---(bossbadi) change bot presence message---#
        elif command.startswith('=p.change'):
            if userid == ADMIN_ID:
                pres = raw_content[9:].strip()
                if pres:
                    game = discord.Game(pres)
                    await client.change_presence(activity=game)
                    await message.channel.send("Presence changed.")
                else:
                    await message.channel.send(CANNOT_SEND_EMPTY_MSG)

        # ---(bossbadi) reset bot presence message---#
        elif command.startswith('=p.reset'):
            if userid == ADMIN_ID:
                game = discord.Game(f"=help | {len(client.guilds)} servers")
                await client.change_presence(activity=game)
                await message.channel.send("Presence has been reset.")


        # ---(bossbadi) eval command (can shutdown bot)---#
        elif command.startswith('=eval'):
            if userid == ADMIN_ID:
                code = raw_content[5:].strip()
                if code: eval(code)


        # ---(bossbadi) log messages toggle---#
        elif command.startswith('=tog'):
            if userid == ADMIN_ID:
                if log_msgs:
                    log_msgs = False
                else:
                    log_msgs = True
                await message.channel.send(f"Toggle: `{log_msgs}`")


        elif command.startswith('=guilds'):
            if userid == ADMIN_ID:  # prints bot servers details
                with open('guilds.txt', 'w') as f:
                    for g in client.guilds:
                        row = (g.id, g.name, g.member_count)
                        f.write(str(row) + '\n')
                try:
                    await message.author.create_dm()
                    await message.author.dm_channel.send(file=discord.File('guilds.txt'))
                except:
                    pass


        elif command.startswith('=glog'):  # bot joins/leaves guild
            if userid == ADMIN_ID:  # prints bot servers details
                guilds_str = ""
                if recent_guilds:
                    for g in reversed(recent_guilds):
                        if len(guilds_str + f"{g}\n") <= 2000:
                            guilds_str += f"{g}\n"
                        else:
                            break
                else:
                    guilds_str = "Did not join or leave any new servers yet."

                recent_guilds.clear()

                try:
                    await message.author.create_dm()
                    await message.author.dm_channel.send(guilds_str)
                except:
                    pass


        elif command.startswith('=lget'):  # get all log.txt file DMed
            if userid == ADMIN_ID: # prints bot servers details
                try:
                    await message.author.create_dm()
                    await message.author.dm_channel.send(file=discord.File('log.txt'))
                except: pass
                await cooldown_end(userid)
                return

        elif command.startswith('=ldel'):  # delete log.txt
            if userid == ADMIN_ID: # prints bot servers details
                if os.path.isfile('log.txt'):
                    try:
                        os.remove('log.txt')
                    except PermissionError:
                        pass
                await message.channel.send("Done.")


        # ---command list---#
        elif content == "=help" or content == "=h":
            embed = embed_help(discord)
            await message.channel.send(embed=embed)


        # ---essentials---#
        elif command.startswith('=ping'):
            latency = round(client.latency * 1000, 3)
            await message.channel.send(f":ping_pong: Pong! `{latency} ms`")


        elif command.startswith('=flip') or command.startswith('=coin'):
            num = random.randint(0, 1)
            if num == 0: msg = ":coin: Heads!"
            else: msg = ":coin: Tails!"
            await message.channel.send(msg)


        elif command.startswith('=roll') or command.startswith('=dice'):
            num = random.randint(1, 6)
            await message.channel.send(f":game_die: {num}")


        elif command.startswith('=rand'):
            RAND_WRONG = ":face_with_raised_eyebrow: That's not how it's done. `=rand <Start> <End>`, for example, `=rand 1 100`"
            raw_input = raw_content[5:].strip().split(' ')
            if len(raw_input) == 2:
                ranges = []
                for num in raw_input:
                    if num[-1].isdigit():
                        try:
                            ranges.append(int(num))
                        except:
                            await message.channel.send(RAND_WRONG)
                            await cooldown_end(userid)
                            return
                    else:
                        await message.channel.send(RAND_WRONG)
                        await cooldown_end(userid)
                        return

                ranges.sort()
                try:
                    rand_num = random.randint(int(ranges[0]), int(ranges[1]))
                except:
                    rand_num = RAND_WRONG
                await message.channel.send(rand_num)
            else:
                await message.channel.send(RAND_WRONG)


        # ---calculator---#
        elif command.startswith('=c') or command.startswith('=calc'):
            has_ping, discord_user_id = check_for_ping(content, userid)
            if discord_user_id:
                if isinstance(discord_user_id, int):  # checking if it's a real member'
                    try:
                        discord_user = await message.guild.fetch_member(discord_user_id)
                    except:
                        discord_user = None
                    if discord_user: has_ping = True

            if not has_ping:
                ans = scrape_math(content)
                if ans:
                    await message.channel.send(ans)
                else:
                    await message.channel.send("You have to input something for me to calculate!")
            else:
                await message.channel.send(":face_with_raised_eyebrow: I'm not pinging anyone.")


        elif command.startswith('=graph'):  # graphing ordered pairs
            data = raw_content[6:].strip()
            if not data:
                await message.channel.send(":face_with_raised_eyebrow: What am I graphing? `=graph <Ordered pairs>`")
                await cooldown_end(userid)
                return

            result = get_devs(userid=userid, data=data)
            if result:
                if result.startswith(":"):
                    await message.channel.send(result)
                else:  # sending the graph
                    await message.channel.send(file=discord.File(result))  # sending the image

                    if os.path.isfile(result):
                        try: os.remove(result)
                        except PermissionError: pass


        # ---about the bot---#
        elif command.startswith('=about'):
            await message.channel.send(embed=embed_about(discord, a_talk, BOT_LOG))


        await cooldown_end(userid)


    except Exception as e:
        await cooldown_end(str(message.author.id))
        print(traceback.format_exc())
        try: await message.channel.send(str(e))
        except: pass


if __name__ == "__main__":
    client.run(TOKEN)
