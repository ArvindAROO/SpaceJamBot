
import discord
from discord.ext import commands
import os
from time import sleep
intents = discord.Intents().all()
token = "insert token here"
Bot = commands.Bot(command_prefix=".", help_command=None, intents=intents)

SPACEJAM = 799316397577863227 #Server id
BOT_TEST = 803621765506400348 #channel id for bot stuff

def isValidGroupName(GroupName):
    #verify if team name actuallly has a name and number
    if(len(GroupName)) < 2:
        return [False, []]
    try:
        no = int(GroupName[-1])
        Name = ' '.join(GroupName)
        return [True, [Name, no]]
    except ValueError:
        return [False, []]



@Bot.event
async def on_command_error(ctx, error):
    # error handling, in case of an error the error message will be put up in the channel
    string = "Something's wrong, I can feel it\n"
    string += str(error)
    channel = ctx.channel
    await Bot.get_channel(BOT_TEST).send( string + '\n' +
        str(ctx.message.author) + " made this mistake in " + str(channel)
    )

@Bot.command(aliases=["p", "purge"])
async def _clear(ctx, amt=0):
    rls = [r.name for r in ctx.author.roles]
    if ("core" in rls) or ("Mod" in rls):
        if(amt<=0):
            await ctx.channel.send("how much you want to purge")
        await ctx.channel.purge(limit=amt)

    else:
        await ctx.channel.send(f"{ctx.author.mention} You do not have the permissions to execute this command")
        return
@Bot.event
async def on_ready():
    await Bot.get_channel(BOT_TEST).send("Bot is online")
    

@Bot.event
async def on_member_join(member):
    welcome = 807099825740185601 #welcome channel for greeting
    await Bot.get_channel(welcome).send("Welcome to SpaceJam server"+ member.mention + ", How are you?\nType `.h` whenever you need any help\nVisit <#807101180341387265> to have a look at the rules and happy coding")
    
    role = discord.utils.get(member.guild.roles, id = 814123158276800583) #give them `Unverified` role
    await member.add_roles(role)


@Bot.event
async def on_member_remove(user):
    await Bot.get_channel(BOT_TEST).send(str(user) + " just left.")
    await Bot.get_channel(BOT_TEST).send(str(user.mention) + " just left.")
@Bot.command(aliases = ['i', 'Info'])
async def info(ctx):
    #A command to get info about the server
    for guild in Bot.guilds:
        await ctx.send("I am in channel "+guild.name)
        await ctx.send("We have {} people here, wow!!".format(len(guild.members)))
    
@Bot.command(aliases = ['remind'])
async def _remind(ctx, mins:int):
    # send the notification to all team channels, ie all channels of name 'discussions' 
    # mins is the number of mins left for submission
    admin = discord.utils.get(ctx.guild.roles, name="core")
    mods = discord.utils.get(ctx.guild.roles, name="Mod")
    if ((admin in ctx.author.roles) or (mods in ctx.author.roles)):
            
        channelsList = []
        for server in Bot.guilds:
            count = 0
            for channel in server.channels:
                channelName = str(channel.name)
                if 'cussion' in channelName.lower():
                    count+=1
                    channelsList.append(channel.id)
            break
        for id in channelsList:
            await Bot.get_channel(id).send("hey guys, the submissions end in {} mins, the only allowed platform for video is YOUTUBE, pls fill ASAP".format(mins))
        await ctx.send("Done for {} channels".format(count))
    else:
        await ctx.send("You dont have the perms for that lmao")

@Bot.command(aliases = ['promote'])
async def _promote(ctx):
    if ctx.author.id == 718845827413442692: #hmm, only i can do this
        await ctx.send("https://tenor.com/view/hello-madagascar-gif-9404174")
        await ctx.send("Hey everyone, it was awesome to be a part of such a big hackathon. If you like me, do check out my source code at https://github.com/ArvindAROO/SpaceJamBot")

@Bot.command(aliases = ['help', 'h', 'Help', 'H'])
async def _help(ctx, *params):
    string = "Hello!!!\nI am Julien bot for SpaceJam, ping `@mentors` or `@core` or `@organisers` if you have any problems. "
    await ctx.channel.send(string)


@Bot.command(aliases=["c", "count"])
async def _count(ctx, *roleName):
    roleName = " ".join(roleName)
    # convert it back into string and split it at '&' and strip the individual roles
    try:
        roleName = roleName.split("&")
    except:
        pass
    temp = []
    for i in roleName:
        temp.append(i.strip())
    roleName = temp
    await ctx.send("Got request for role " + str(roleName))
    # A command to get number of users in a role
    if roleName == [""]:
        for guild in Bot.guilds:
            await ctx.send("We have {} people here, wow!!".format(len(guild.members)))
    else:
        thisRole = []
        # make a list of all roles in terms of role-id
        for roles in roleName:
            thisRole.append(discord.utils.get(ctx.guild.roles, name=roles))
        for guild in Bot.guilds:
            count = 0
            for member in guild.members:
                boolean = True
                # bool will be true only if all the roles passed as args are present
                for roles in thisRole:
                    if roles not in member.roles:
                        boolean = False
                if boolean:
                    count += 1
        await ctx.send(str(count) + " people has role " + str(thisRole))

@Bot.command(aliases = ['ping'])
async def _test(ctx):
    #return latency of the bot
    string = "Pong!!!\nPing = " + str(round(Bot.latency * 1000)) + "ms"
    await ctx.send(string)

@Bot.command(case_insensitive = True, aliases = ['Julien'])
async def _Julian(ctx):
    # a small easter egg
    await ctx.send("https://tenor.com/view/madagascar-king-julien-move-it-move-i-like-to-move-it-gif-4835667")



@Bot.command(aliases = ['rules'])
async def _rules(ctx):
    string = """
```markdown
#General Rules
1. No Spam or flooding the chat with messages. Any kind of spam pinging, roles or users will not be tolerated and will result in instant ban.
2. No bashing or heated arguments to other people in the chat. Toxicity will not be tolerated
3. No adult (18+), explicit, or controversial messages.
4. No racism or degrading content.
5. This server is only for the hackathon. If you are not part of it, do not join. And participants are not allowed to forward the invite link to random people.
6. No offensive names.
7. Do not perform or promote the intentional use of glitches, hacks, bugs, and other exploits that will cause an incident within the community and other participants.
8. In case of any issue, problem or if help required, ping @organizers and wait for them to respond. Do not repeatedly ping anyone
9. In case of any discord issues, missing permissions or wrong team assignment, ping @Mods or @Mentors

#Voice Chat Rules
1. No voice chat surfing or switching channels repeatedly.
2. No annoying, loud or high pitch noises.
3. Reduce the amount of background noise, if possible. Resort to push to talk in your settings to reduce the issue.
4. Joining other peoples VC is not allowed```"""
    
    await ctx.send(string)


@Bot.command(case_insensitive = True,aliases = ["addGroup", "ag"])
async def _add_Group(ctx, user1: discord.Member = None, user2: discord.Member = None,user3: discord.Member = None,user4: discord.Member = None, *GroupName):
    #command to generate team and role and a seperate category containing a Text and Vc for that team
    
    #the syntax must be `.ag user1 user2 user3 user4 teamname teamnumber`
    #even if the team doesnt contain 4, repeat mentioning the same members
    admin = discord.utils.get(ctx.guild.roles, name="core")
    mods = discord.utils.get(ctx.guild.roles, name="Mod")
    try:
        if GroupName == []:
            await ctx.send("Please enter a valid groupname")
            return
        if user1 == None:
            await ctx.send("The group cant be empty")
        if ((admin in ctx.author.roles) or (mods in ctx.author.roles)):
            guild = Bot.get_guild(SPACEJAM)
            res = isValidGroupName(GroupName)
            await ctx.send("Got request for role {}".format(res[1][0]))
            if res[0]:
                GroupNameFinal = res[1][0]
                author = ctx.message.author
                await guild.create_role(name=GroupNameFinal)
                sleep(0.5)
                role = discord.utils.get(ctx.guild.roles, name=GroupNameFinal)
                await ctx.send("Created role {}".format(role.mention))
                if user1:
                    await user1.add_roles(role)
                if user2:
                    await user2.add_roles(role)
                if user3:
                    await user3.add_roles(role)
                if user4:
                    await user4.add_roles(role)
                await ctx.send("Added roles")
                category = await ctx.guild.create_category(GroupNameFinal)
                await ctx.send("created category called {}".format(GroupNameFinal))
                #create category and set perms
                await category.set_permissions(role, read_messages=True, connect=True,attach_files = True,  speak = True, stream = True, read_message_history = True)
                await category.set_permissions(admin, read_messages=True, connect=True,attach_files = True,  speak = True, stream = True, read_message_history = True)
                await category.set_permissions(mentors, read_messages=True, connect=True,attach_files = True,  speak = True, stream = True, read_message_history = True)
                await category.set_permissions(ctx.guild.default_role, view_channel=False, create_instant_invite=False) #disallow everyone there and allow only that team, mentors and core
                #add channels into that
                await ctx.guild.create_text_channel('Discussions', category=category, sync_permissions=True)
                await ctx.guild.create_voice_channel('VC', category=category, sync_permissions=True)

                
            else:
                #in case the syntax was wrong
                await ctx.send("The groupname seems to be in wrong format, please provide it in `GroupName GroupNumber` format only")
        else:
            #only mods and core could do this
            await ctx.send("{} You dont have the perms to do that, contact moderators for any help".format(ctx.message.author.mention))
    except Exception as E:
        await ctx.send(E)

@Bot.command(aliases = ['say'])
async def channel_welcome(ctx):
    # a warm welcome msg to say in the new channel
    await ctx.send("Hey guys, welcome to Spacejam. This is your team channel and there's a voice channel as well. If you have any doubts, ping someone from the core team who is online at the moment. Happy Hacking!")


@Bot.command(aliases = ['verify', 'v'])
async def _verify(ctx, roleName):
    #remove the `Unverified` role and add `Verified` role
    admin = discord.utils.get(ctx.guild.roles, name="core")
    mentors = discord.utils.get(ctx.guild.roles, name = "mentor")
    mods = discord.utils.get(ctx.guild.roles, name="Mod")
    
    Verified = discord.utils.get(ctx.author.guild.roles, id = 815050646993633315)
    Unverified = discord.utils.get(ctx.author.guild.roles, id = 814123158276800583)
    strOfRole = ''
    if ((admin in ctx.author.roles) or (mods in ctx.author.roles) or (mentors in ctx.author.roles)):
        #either mentor/core/mod can do this
        for i in roleName:
            if i in '0123456789':
                strOfRole += i
        #easiest way to find if role exists, checks if they all are int
        roleName = discord.utils.get(ctx.author.guild.roles, id = int(strOfRole))
        for guild in Bot.guilds:
            count = 0
            for member in guild.members:
                #if the member has that team role, remove unverified and add verified
                if roleName in member.roles:
                    count += 1
                    await member.add_roles(Verified)
                    await member.remove_roles(Unverified)
        await ctx.send("Task done for {} members".format(count))
      


Bot.run(token)
