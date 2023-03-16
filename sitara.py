import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
import json
from discord.ui import Button, View
import datetime
load_dotenv()

bot = commands.Bot(command_prefix="s.", case_insensitive=True, help_command=None, intents=discord.Intents.all())
bot_token = os.getenv("DISCORD_BOT_TOKEN")
with open("guilddata.json", "r") as f:
    gdata = json.load(f)

@bot.event
async def on_ready():
    print("I am ready")


@bot.command(name="set-starboard", aliases=['sb'])
@commands.has_permissions(administrator=True)
async def setstar(ctx, chnl: str=None):
    try:
        if chnl is None:
            chnl_obj = ctx.channel
        else:
            chnl_obj = await commands.TextChannelConverter().convert(ctx, chnl)
    except commands.errors.ChannelNotFound:
        errorembed = discord.Embed(description="Invalid channel specified", color=0xFF0000)
        await ctx.reply(embed = errorembed)
        return
    if str(ctx.guild.id) not in gdata.keys():
        gdata[str(ctx.guild.id)] = {'sbchannel': chnl_obj.id, 'sbmessages': [], 'star_count': 5}
    else:
        gdata[str(ctx.guild.id)]['sbchannel'] = chnl_obj.id
        gdata[str(ctx.guild.id)]['sbmessages'] = []
    setembed = discord.Embed(description=f"Starboard channel was set to <#{chnl_obj.id}>", color=0x00FF00)
    await ctx.reply(embed = setembed)
    with open("guilddata.json", "w") as f:
        json.dump(gdata, f, indent=4)

@bot.command(name="set-count", aliases=['sc'])
@commands.has_permissions(administrator=True)
async def sc(ctx, count=None):
    if ctx.author.bot:
        return
    try:
        if count is None:
            error_embed = discord.Embed(description="Star count is required argument", color=0xFF0000)
            await ctx.reply(embed=error_embed)
            return
        count = int(count)
    except ValueError:
        error_embed = discord.Embed(description="You need to enter an `Integer`", color=0xFF0000)
        await ctx.reply(embed=error_embed)
        return

    if str(ctx.guild.id) not in gdata.keys():
        error_embed = discord.Embed(description="Please set the starboard channel first using `s.sb`", color=0xFF0000)
        await ctx.reply(embed=error_embed)
    if count < 1:
        error_embed = discord.Embed(description="Minimum value for star count is 1", color=0xFF0000)
        await ctx.reply(embed=error_embed)
        return
    gdata[str(ctx.guild.id)]['star_count'] = count
    sembed = discord.Embed(description=f"Star count set to **{count}**", color=0x00FF00)
    await ctx.reply(embed=sembed)
    with open("guilddata.json", "w") as f:
        json.dump(gdata, f, indent=4)

@bot.event
async def on_reaction_add(reaction, user):
    msg = reaction.message
    if str(msg.guild.id) not in gdata.keys():
        return
    sbchannel = discord.utils.get(msg.guild.text_channels, id=gdata[str(msg.guild.id)]['sbchannel'])
    if reaction.emoji != "⭐":
        return
    if reaction.count >= gdata[str(str(msg.guild.id))]['star_count']:
        if msg.id in gdata[str(msg.guild.id)]['sbmessages']:
            return
        else:
            view = View()
            jumpbut = Button(style=discord.ButtonStyle.link, url=msg.jump_url, label="Jump to Message")
            view.add_item(jumpbut)
            av = msg.author.avatar
            if av is None:
                av = msg.author.default_avatar
            sbembed = discord.Embed(description=msg.content, color=0x00FFFF)
            sbembed.set_author(name=f"{msg.author.name}#{msg.author.discriminator}", icon_url=av)
            sbembed.set_footer(text=f"Message Id: {msg.id} | {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}")
            gdata[str(msg.guild.id)]['sbmessages'].append(msg.id)
            if msg.attachments:
                sbembed.video.url = msg.attachments[0].url
                sbembed.set_image(url=msg.attachments[0].url)
                await sbchannel.send(content=f"⭐ | <@{msg.author.id}>", embed=sbembed, view=view)
            else:
                await sbchannel.send(content=f"⭐ | <@{msg.author.id}>", embed=sbembed, view=view)
    with open("guilddata.json", "w") as f:
        json.dump(gdata, f, indent=4)

@bot.command(name="starit")
@commands.has_permissions(administrator=True)
async def starit(ctx, msgid: str=None):
    if ctx.author.bot:
        return
    try:
        if msgid is not None:
            msg_obj = await commands.MessageConverter().convert(ctx, argument=msgid)
        else:
            if not ctx.message.reference:
                errorembed = discord.Embed(description="Please reply to the message you want to star or mention its `message_id`", color=0xFF0000)
                await ctx.reply(embed=errorembed)
                return
            else:
                msg_obj = await ctx.channel.fetch_message(ctx.message.reference.message_id)
    except commands.errors.MessageNotFound:
        errorembed = discord.Embed(description="Invalid `message_id` specified or message deleted", color=0xFF0000)
        await ctx.reply(embed=errorembed)
        return

    if str(msg_obj.guild.id) not in gdata.keys():
        errorembed = discord.Embed(description="Please setup your server for star board.", color=0xFF0000)
        await ctx.reply(embed=errorembed)
        return

    sbchannel = discord.utils.get(msg_obj.guild.text_channels, id=gdata[str(msg_obj.guild.id)]['sbchannel'])

    if msg_obj.id in gdata[str(msg_obj.guild.id)]['sbmessages']:
        errorembed = discord.Embed(description="Message already in star board.", color=0xFF0000)
        await ctx.reply(embed=errorembed)
        return
    else:
        view = View()
        jumpbut = Button(style=discord.ButtonStyle.link, url=msg_obj.jump_url, label="Jump to Message")
        view.add_item(jumpbut)
        av = msg_obj.author.avatar
        if av is None:
            av = msg_obj.author.default_avatar
        sbembed = discord.Embed(description=msg_obj.content, color=0x00FFFF)
        sbembed.set_author(name=f"{msg_obj.author.name}#{msg_obj.author.discriminator}", icon_url=av.url)
        sbembed.set_footer(text=f"Message Id: {msg_obj.id} | {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}")
        if msg_obj.attachments:
            sbembed.video.url = msg_obj.attachments[0].url
            sbembed.set_image(url=msg_obj.attachments[0].url)
            await sbchannel.send(content=f"⭐ | <@{msg_obj.author.id}>", embed=sbembed, view=view)
        else:
            await sbchannel.send(content=f"⭐ | <@{msg_obj.author.id}>", embed=sbembed, view=view)

    gdata[str(msg_obj.guild.id)]['sbmessages'].append(msg_obj.id)
    with open("guilddata.json", "w") as f:
        json.dump(gdata, f, indent=4)

@bot.command(name="help")
async def help(ctx):
    if ctx.author.bot:
        return
    hembed = discord.Embed(title="Help Command", description="This is the help command for **Sitara** bot. A simple starboard bot which you can setup to star messages", color=0x00FFFF)
    hembed.set_thumbnail(url=ctx.bot.user.display_avatar.url)
    hembed.add_field(name="Command Usage", value=f"```\ns.set-starboard <chanel_id/channel_name>\ns.set-count [star_count]\ns.starit <message_id>```")
    await ctx.reply(embed=hembed)


bot.run(bot_token)