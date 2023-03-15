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

@bot.command(name="test")
async def test(ctx):
    await ctx.reply("Hello")

@bot.command(name="sb")
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
    if ctx.guild.id not in gdata.keys():
        gdata[str(ctx.guild.id)] = {'sbchannel': chnl_obj.id, 'sbmessages': []}
    else:
        gdata[str(ctx.guild.id)]['sbchannel'] = chnl_obj.id
    setembed = discord.Embed(description=f"Starboard channel was set to <#{chnl_obj.id}>", color=0x00FF00)
    await ctx.reply(embed = setembed)
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
    if reaction.count >= 1:
        if msg.id in gdata[str(msg.guild.id)]['sbmessages']:
            return
        else:
            av = msg.author.avatar
            if av is None:
                av = msg.author.default_avatar
            if msg.attachments:
                view = View()
                jumpbut = Button(style=discord.ButtonStyle.link, url=msg.jump_url, label="Jump to Message")
                view.add_item(jumpbut)
                sbembed = discord.Embed(description=msg.content, color=0x00FFFF)
                sbembed.video.url = msg.attachments[0].url
                sbembed.set_image(url=msg.attachments[0].url)
                sbembed.set_author(name=msg.author.name, icon_url=av)
                sbembed.set_footer(text=f"Message Id: {msg.id} | {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}")
                await sbchannel.send(content=f"⭐ | <@{msg.author.id}>", embed=sbembed, view=view)
            else:
                view = View()
                jumpbut = Button(style=discord.ButtonStyle.link, url=msg.jump_url, label="Jump to Message")
                view.add_item(jumpbut)
                sbembed = discord.Embed(description=msg.content, color=0x00FFFF)
                sbembed.set_author(name=f"{msg.author.name}#{msg.author.discriminator}", icon_url=av)
                sbembed.set_footer(text=f"Message Id: {msg.id} | {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}")
                await sbchannel.send(content=f"⭐ | <@{msg.author.id}>", embed=sbembed, view=view)
    gdata[str(msg.guild.id)]['sbmessages'].append(msg.id)
    with open("guilddata.json", "w") as f:
        json.dump(gdata, f, indent=4)



bot.run(bot_token)