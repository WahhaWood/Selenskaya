
import disnake
from disnake.ext import commands
from pymongo import MongoClient
import config as con

bot = commands.Bot(command_prefix="*", intents = disnake.Intents.all())
cluster = MongoClient(con.MONGODB_URL)
db = cluster.botdb
coll = db.clans
clans = cluster.botdb.clans
channels = cluster.botdb.channels
invites = cluster.botdb.invites
repa = "🔰"
p = "*"

@bot.event
async def on_ready():
	print(f'[BOT] Бот {bot.user.name} запущен')

@bot.event
async def on_message(message):
	await bot.process_commands( message )
	if clans.find_one({"members": message.author.name}):
		coll.update_one({"members": message.author.name}, {'$inc': {'rep': 0.5}})
	if clans.find_one({"owner": message.author.id}):
		coll.update_one({"owner": message.author.id}, {'$inc': {'rep': 0.5}})



@bot.command(aliases=['c-create'])
async def c_create(ctx,*, name: str = None):
	channel_obj = channels.find_one({"name": "Selenskaya"})
	if ctx.channel.id in channel_obj["channels"]:
		return await ctx.send(embed = disnake.Embed(
			title=":x: Возникла ошибка :x:",
			description="Вы не можете использовать бота в этом канале! \n `Администрация запретила использовать бота в этом канале`",
			color = disnake.Colour.red()
		))

	query = {"name": name}
	for value in coll.find(query):
		return await ctx.send(embed = disnake.Embed(
			title=":x: Возникла ошибка :x:",
			description="Клан с таким названием уже существует! \n `Используйте другое название для клана`",
			color = disnake.Colour.red()
				))
	if clans.count_documents({"owner": ctx.author.id}) or clans.count_documents({"members": ctx.author.name}):
		return await ctx.send(embed = disnake.Embed(
			title=":x: Возникла ошибка :x:",
			description="Вы уже состоите в клане! \n `Покиньте клан перед использованием этой команды`",
			color = disnake.Colour.red()
				))


	if not name:
		return await ctx.send(embed = disnake.Embed(
			title=":x: Возникла ошибка :x:",
			description=f"Вы не указали название клана! \n **Использование** \n> `{p}c-create [Название клана]` \n **Пример** \n> `{p}c-create Selenskaya`",
			color = disnake.Colour.red()
				))


	if not ctx.guild.get_role(863035902829527040) in ctx.author.roles:
		await ctx.send(embed = disnake.Embed(
			title=":x: Возникла ошибка :x:",
			description="Вы не можете создать клан без роли <@&863035902829527040>!",
			color = disnake.Colour.red()
				))
	
	if ctx.guild.get_role(863035902829527040) in ctx.author.roles:
		post = {
    			"name": name,
    			"rep": 0,
    			"owner": ctx.author.id,
    			"members": [],
				"invite": "allow"
			}

		post_2 = {
    			"name": name,
    			"invites":[]
			}
		clans.insert_one(post)
		invites.insert_one(post_2)
		await ctx.send(embed = disnake.Embed(
    		title=":white_check_mark: Все прошло успешно :white_check_mark:",
			description=f"Клан **{name}** успешно создан!\n**Узнать информацию о клане**\n> `{p}c-info {name}` ",
    		color = disnake.Colour.green()
    			 ))
	
	
@bot.command(aliases=['c-info'])
async def c_info(ctx,*, name: str = None):
	channel_obj = channels.find_one({"name": "Selenskaya"})
	if ctx.channel.id in channel_obj["channels"]:
		return await ctx.send(embed = disnake.Embed(
			title=":x: Возникла ошибка :x:",
			description="Вы не можете использовать бота в этом канале! \n `Администрация запретила использовать бота в этом канале`",
			color = disnake.Colour.red()
		))
	
	if not name:
		return await ctx.send(embed = disnake.Embed(
			title=":x: Возникла ошибка :x:",
			description=f"Вы не указали название клана! \n **Использование** \n> `{p}c-info [Название клана]` \n **Пример** \n> `{p}c-info Selenskaya`",
			color = disnake.Colour.red()
				))

	clan_obj = clans.find_one({"name": name})
	if not clan_obj:
		return await ctx.send(embed = disnake.Embed(
			title=":x: Возникла ошибка :x:",
			description="Клана с таким названием не существует!",
			color = disnake.Colour.red()
				))


	clan_obj = clans.find_one({"name": name})
	okay = len(coll.find_one({"name": name})['members'])
	embed = disnake.Embed(title = name,color = disnake.Colour.blue())
	embed.add_field(name="💠 Владелец", value= f"> {ctx.guild.get_member(clan_obj['owner'])}", inline=False)
	embed.add_field(name="👥 Всего участников", value= f"> {okay}", inline=False)
	embed.add_field(name=f"{repa} Репутация", value = f"> {clan_obj['rep'] if clan_obj['rep'] else '0'} {repa}" , inline=False)
	return await ctx.send(embed=embed)

@bot.command(aliases=['c-join'])
async def c_join(ctx,*, name: str = None):
	channel_obj = channels.find_one({"name": "Selenskaya"})
	if ctx.channel.id in channel_obj["channels"]:
		return await ctx.send(embed = disnake.Embed(
			title=":x: Возникла ошибка :x:",
			description="Вы не можете использовать бота в этом канале! \n `Администрация запретила использовать бота в этом канале`",
			color = disnake.Colour.red()
		))

	if not name:
		return await ctx.send(embed = disnake.Embed(
			title=":x: Возникла ошибка :x:",
			description=f"Вы не указали название клана! \n **Использование** \n> `{p}c-join [Название клана]` \n **Пример** \n> `{p}c-join Selenskaya`",
			color = disnake.Colour.red()
				))
	clan_obj = clans.find_one({"name": name})
	if not clan_obj:
		return await ctx.send(embed = disnake.Embed(
			title=":x: Возникла ошибка :x:",
			description="Клана с таким названием не существует!",
			color = disnake.Colour.red()))

	if clans.find_one({"name": name})['invite'] == 'deny':
		return await ctx.send(embed = disnake.Embed(
			title=":x: Возникла ошибка :x:",
			description=f"Используйте команду: \n> `{p}c-invite {name}`",
			color = disnake.Colour.red()
				))

	if clans.count_documents({"owner": ctx.author.id}) or clans.count_documents({"members": ctx.author.name}):
		return await ctx.send(embed = disnake.Embed(
			title=":x: Возникла ошибка :x:",
			description="Вы уже состоите в клане! \n `Покиньте клан перед использованием этой команды`",
			color = disnake.Colour.red()
				))



	if clans.find_one({"name": name})['invite'] == 'allow':
		clan_obj['members'].append(ctx.author.name)
		clans.update_one({"name": name}, {"$set":{'members': clan_obj['members']}})
		await ctx.send(embed = disnake.Embed(
			title=":white_check_mark: Все прошло успешно :white_check_mark:",
			description=f"Вы успешно присоиденились к клану **{name}**!",
			color = disnake.Colour.green()
				 ))

@bot.command(aliases=['c-top'])
async def c_top(ctx):
	channel_obj = channels.find_one({"name": "Selenskaya"})
	if ctx.channel.id in channel_obj["channels"]:
		return await ctx.send(embed = disnake.Embed(
			title=":x: Возникла ошибка :x:",
			description="Вы не можете использовать бота в этом канале! \n `Администрация запретила использовать бота в этом канале`",
			color = disnake.Colour.red()
		))

	embed = disnake.Embed(title="⚔ |Selenskaya: Топ-10 кланов по репутации", description="Фильтрация по **количеству репутации** \n Подробнее о гильдии: `=c-info [Название]` \n Всупить в гильдию: `=c-join [Название]`",  color=disnake.Color.orange())
	i = 0

	clans2 = clans.find().sort([
	("reps", -1)
	]).limit(10)

	for clan in clans2:
		owner = ctx.guild.get_member(clan['owner'])
		try:
			i += 1
			embed.add_field(name=f"{i}. {clan['name']}", value=f"Репутация: {clan['rep'] if clan['rep'] else '0'} {repa}", inline=False)
		except Exception as e:
			print(e)
			i -= 1
	await ctx.send(embed=embed)

		

@bot.command(aliases=['c-leave'])
async def c_leave(ctx, *, name: str = None):
	channel_obj = channels.find_one({"name": "Selenskaya"})
	if ctx.channel.id in channel_obj["channels"]:
		return await ctx.send(embed = disnake.Embed(
			title=":x: Возникла ошибка :x:",
			description="Вы не можете использовать бота в этом канале! \n `Администрация запретила использовать бота в этом канале`",
			color = disnake.Colour.red()
		))

	if not name:
		return await ctx.send(embed = disnake.Embed(
			title=":x: Возникла ошибка :x:",
			description=f"Вы не указали название клана! \n **Использование** \n> `{p}c-leave [Название клана]` \n **Пример** \n> `{p}c-leave Selenskaya`",
			color = disnake.Colour.red()
				))
	clan_obj = clans.find_one({"name": name})
	if not clan_obj:
		return await ctx.send(embed = disnake.Embed(
			title=":x: Возникла ошибка :x:",
			description="Клана с таким названием не существует!",
			color = disnake.Colour.red()))

	if clans.find_one({"owner": ctx.author.id}):
		return await ctx.send(embed = disnake.Embed(
			title=":x: Возникла ошибка :x:",
			description="Вы не можете выйти из клана который вы создали!",
			color = disnake.Colour.red()
				))


	clan_obj['members'].remove(ctx.author.name)
	clans.update_one({"name": name}, {"$set":{"members": clan_obj['members']}})
	return await ctx.send(embed = disnake.Embed(
			title=":white_check_mark: Все прошло успешно :white_check_mark:",
			description=f"Вы покинули клан **{name}**!",
			color = disnake.Colour.green()
			))



@bot.command(aliases=['c-delete'])
async def c_delete(ctx,*, name: str = None):
	channel_obj = channels.find_one({"name": "Selenskaya"})
	if ctx.channel.id in channel_obj["channels"]:
		return await ctx.send(embed = disnake.Embed(
			title=":x: Возникла ошибка :x:",
			description="Вы не можете использовать бота в этом канале! \n `Администрация запретила использовать бота в этом канале`",
			color = disnake.Colour.red()
		))

	if not name:
		return await ctx.send(embed = disnake.Embed(
			title=":x: Возникла ошибка :x:",
			description=f"Вы не указали название клана! \n **Использование** \n> `{p}c-delete [Название клана]` \n **Пример** \n> `{p}c-delete Selenskaya`",
			color = disnake.Colour.red()
				))

	if not clans.find_one({"name": name}):
		return await ctx.send(embed = disnake.Embed(
			title=":x: Возникла ошибка :x:",
			description="Клана с таким названием не существует! ",
			color = disnake.Colour.red()))

	qerry = {"name": name, "owner": ctx.author.id}
	if clans.find_one({"name": name})["owner"] == ctx.author.id:
		await ctx.send(embed = disnake.Embed(
			title=":white_check_mark: Все прошло успешно :white_check_mark:",
			description=f"Клан **{name}** был удалён!",
			color = disnake.Colour.green()
				))
		clans.delete_one({'name': name})

	else:
		await ctx.send(embed = disnake.Embed(
			title=":x: Возникла ошибка :x:",
			description="Вы не можете удалить этот клан",
			color = disnake.Colour.red()
				))


@bot.command(aliases=['c-perm'])
async def c_perm(ctx, bbc, channel):
	channel_name = int(channel.strip("<#>"))
	name = "Selenskaya"
	channels_arr = channels.find_one({"name": name})['channels']

	if bbc == 'allow':
		if channel_name in channels_arr:
			return await ctx.send(embed = disnake.Embed(
			title=":x: Возникла ошибка :x:",
			description="Этого канала нету в списке заблокированных!",
			color = disnake.Color.red()))

		else:
			channel_name = int(channel.strip("<#>"))
			name = "Selenskaya"
			channels_arr = channels.find_one({"name": name})['channels']
			channels_arr.remove(channel_name)
			channels.update_one({"name": name}, {"$set":{"channels": channels_arr}})
			return await ctx.send(embed = disnake.Embed(
			title=":white_check_mark: Все прошло успешно :white_check_mark:",
			description = f"Вы убрали <#{channel_name}> из списка заблокированых канналов",
			color = disnake.Colour.green()))

	if bbc == 'deny':
		if channel_name in channels_arr:
			return await ctx.send(embed = disnake.Embed(
			title=":x: Возникла ошибка :x:",
			description="Этот канал уже в списке заблокированных!",
			color = disnake.Color.red()))
		else:
			channel_name = int(channel.strip("<#>"))
			name = "Selenskaya"
			channels_arr = channels.find_one({"name": name})['channels']
			channels_arr.append(channel_name)
			channels.update_one({"name": name}, {"$set":{"channels": channels_arr}})
			return await ctx.send(embed = disnake.Embed(
        		title=":white_check_mark: Все прошло успешно :white_check_mark:",
        		description = f"Вы добавили <#{channel_name}> в список заблокированых канналов",
        		color = disnake.Colour.purple()))
	else:
		return await ctx.send(embed = disnake.Embed(
			title=":x: Возникла ошибка :x:",
			description=f"Вы не указали какой-то параметр! \n **Использование** \n> `{p}c-perm deny [Пинг канала]` \n **Пример** \n> `{p}c-perm [Пинг канала]`",
			color = disnake.Color.red()))


@bot.command(aliases=['c-listfasfas'])
async def c_listfasfas(ctx, *, name = None):
	channel_obj = channels.find_one({"name": "Selenskaya"})
	if ctx.channel.id in channel_obj["channels"]:
		return await ctx.send(embed = disnake.Embed(
			title=":x: Возникла ошибка :x:",
			description="Вы не можете использовать бота в этом канале! \n `Администрация запретила использовать бота в этом канале`",
			color = disnake.Colour.red()
		))

	if not name:
		return await ctx.send(embed = disnake.Embed(
			title=":x: Возникла ошибка :x:",
			description=f"Вы не указали название клана! \n **Использование** \n> ` {p}c-list [Название клана]` \n **Пример** \n> `{p}c-list Selenskaya`",
			color = disnake.Colour.red()
				))

	clan_obj = clans.find_one({"name": name})
	if not clan_obj:
		return await ctx.send(embed = disnake.Embed(
			title=":x: Возникла ошибка :x:",
			description="Клана с таким названием не существует!",
			color = disnake.Colour.red()
				))
	embed = disnake.Embed(title=f"👥 | Участники гильдии {name}", color=disnake.Color.orange())
	i = 0
	clans2 = clans.find({"name": name})
	for clan in clans2:
		try:
			i += 1
			embed.add_field(name=f"{i}.{clan['members']}", value="", inline=False )
		except Exception as e:
			print(e)
			i -= 1

	await ctx.send(embed=embed)

@bot.command(aliases=['c-help'])
async def c_help(ctx):
	channel_obj = channels.find_one({"name": "Selenskaya"})
	if ctx.channel.id in channel_obj["channels"]:
		return await ctx.send(embed = disnake.Embed(
			title=":x: Возникла ошибка :x:",
			description="Вы не можете использовать бота в этом канале! \n `Администрация запретила использовать бота в этом канале`",
			color = disnake.Colour.red()
		))
	
	return await ctx.send(embed = disnake.Embed(
		title="📋 | Список команд",
		description=f"`{p}c-create` - создать клан \n `{p}c-info` - узнать информацию о клане \n `{p}c-join` - присоидениться к клану \n `{p}c-top` - топ кланов на сервере \n `{p}c-leave` - выйти из клана  \n `{p}c-delete` - удалить клан \n `{p}c-c-requests` - список заявок в клан \n `{p}c-invites` - настройка присоиденения в клан только по запросу \n `{p}c-accept` - принять заявку \n `{p}c-decline` - отклонить заявку \n \n **Только для администрации:** \n `{p}c-perm` - настройка запрета бота в некоторых каналах \n ",
		color= disnake.Colour.green()
	))

@bot.command(aliases=['c-invites'])
async def c_invites(ctx,*, bbc, name):
	if bbc == 'allow':
		clans.update_one({"name": name}, {"$set":{"invite": "allow"}})
		return await ctx.send(embed = disnake.Embed(
		title=":white_check_mark: Все прошло успешно :white_check_mark:",
		description = f"Вы разрешили заходить в клан без вашего одобрения",
		color = disnake.Colour.green()))

	if bbc == 'deny':
		clans.update_one({"name": name}, {"$set":{"invite": "deny"}})
		return await ctx.send(embed = disnake.Embed(
            title=":white_check_mark: Все прошло успешно :white_check_mark:",
            description = f"Вы запретили заходить в клан без вашего одобрения",
            color = disnake.Colour.purple()))

	else: 
		return await ctx.send(embed = disnake.Embed(
			title=":x: Возникла ошибка :x:",
			description=f"Вы не указали какой-то параметр! \n **Использование** \n> `{p}c-invites deny [Название клана]` \n **Пример** \n> `{p}c-invites {name}`",
			color = disnake.Color.red()))
@bot.command(aliases=['c-invite'])
async def c_invite(ctx,*, name: str = None):
	channel_obj = channels.find_one({"name": "Selenskaya"})
	if ctx.channel.id in channel_obj["channels"]:
		return await ctx.send(embed = disnake.Embed(
			title=":x: Возникла ошибка :x:",
			description="Вы не можете использовать бота в этом канале! \n `Администрация запретила использовать бота в этом канале`",
			color = disnake.Colour.red()
		))

	if not name:
		return await ctx.send(embed = disnake.Embed(
			title=":x: Возникла ошибка :x:",
			description=f"Вы не указали название клана! \n **Использование** \n> ` {p}c-invite [Название клана]` \n **Пример** \n> ` {p}c-invite Selenskaya`",
			color = disnake.Colour.red()
				))


	if invites.count_documents({'invites': ctx.message.author.name}):
		return await ctx.send(embed = disnake.Embed(
			title=":x: Возникла ошибка :x:",
			description="Вы уже отправили запрос в один из кланов",
			color = disnake.Colour.red()
				))

	if clans.count_documents({"owner": ctx.author.id}) or clans.count_documents({"members": ctx.author.name}):
		return await ctx.send(embed = disnake.Embed(
			title=":x: Возникла ошибка :x:",
			description="Вы уже состоите в клане! \n `Покиньте клан перед использованием этой команды`",
			color = disnake.Colour.red()
				))

	if ctx.message.author.name in invites.find_one({"name": name})['invites']:
		return await ctx.send(embed = disnake.Embed(
			title=":x: Возникла ошибка :x:",
			description="Вы уже отправили запрос в этот клан",
			color = disnake.Colour.red()
				))

	invites_obj = invites.find_one({"name":name})
	invites_obj['invites'].append(ctx.author.name)
	invites.update_one({"name": name}, {"$set":{'invites': invites_obj['invites']}})
	await ctx.send(embed = disnake.Embed(
			title=":white_check_mark: Все прошло успешно :white_check_mark:",
			description=f"Вы успешно отправили заявку в клан **{name}**!",
			color = disnake.Colour.green()
				 ))

@bot.command(aliases=['c-requests'])
async def c_requests(ctx,*, name: str = None):
	channel_obj = channels.find_one({"name": "Selenskaya"})
	if ctx.channel.id in channel_obj["channels"]:
		return await ctx.send(embed = disnake.Embed(
			title=":x: Возникла ошибка :x:",
			description="Вы не можете использовать бота в этом канале! \n `Администрация запретила использовать бота в этом канале`",
			color = disnake.Colour.red()
		))

	if not name:
		return await ctx.send(embed = disnake.Embed(
			title=":x: Возникла ошибка :x:",
			description=f"Вы не указали название клана! \n **Использование** \n> `{p}c-requests [Название клана]` \n **Пример** \n> `{p}c-requests Selenskaya`",
			color = disnake.Colour.red()
				))

	if not clans.find_one({"name": name}):
		return await ctx.send(embed = disnake.Embed(
			title=":x: Возникла ошибка :x:",
			description="Клана с таким названием не существует! ",
			color = disnake.Colour.red()))

	invite = "\n".join(invites.find_one({"name": name})['invites'])
	return await ctx.send(embed = disnake.Embed(
	title=f"**Список заявок в {name}**",
	description=f"{invite if invite else 'Тут пусто'}",
	color = disnake.Colour.orange()
	))

@bot.command(aliases=['c-accept'])
async def c_accept(ctx,*,nik, name: str = None):
	if clans.find_one({"name": name})["owner"] == ctx.message.author.id:
		if nik not in invites.find_one({'name': name})['invites']:
			return await ctx.send(embed = disnake.Embed(
			title=":x: Возникла ошибка :x:",
			description=f"Человек с ником **{nik}** не отправял заявку в клан **{name}**!",
			color = disnake.Colour.red()))

		clan_obj = clans.find_one({"name": name})
		clan_obj['members'].append('nik')
		clans.update_one({"name": name}, {"$set":{'members': clan_obj['members']}})
		await ctx.send(embed = disnake.Embed(
			title=":white_check_mark: Все прошло успешно :white_check_mark:",
			description=f"**{nik}** успешно присоидинен к клану **{name}**!",
			color = disnake.Colour.green()
				 ))
	else: 
		return await ctx.send(embed = disnake.Embed(
	title=f":x: Возникла ошибка :x:",
	description=f"Вы не можете принять заявку **{nik}**!"
	))

@bot.command(aliases=['c-decline'])
async def c_decline(ctx, nik, name):
	channel_obj = channels.find_one({"name": "Selenskaya"})
	if ctx.channel.id in channel_obj["channels"]:
		return await ctx.send(embed = disnake.Embed(
			title=":x: Возникла ошибка :x:",
			description="Вы не можете использовать бота в этом канале! \n `Администрация запретила использовать бота в этом канале`",
			color = disnake.Colour.red()
		))

	if not name:
		return await ctx.send(embed = disnake.Embed(
			title=":x: Возникла ошибка :x:",
			description=f"Вы не указали название клана! \n **Использование** \n> `{p}c-decline [Ник подавшего заявку] [Название клана]` \n **Пример** \n> `{p}c-decline Wahha Selenskaya`",
			color = disnake.Colour.red()
				))

	if not nik:
		return await ctx.send(embed = disnake.Embed(
			title=":x: Возникла ошибка :x:",
			description=f"Вы не указали ник подавшего заявку! \n **Использование** \n> `{p}c-decline [Ник подавшего заявку] [Название клана]` \n **Пример** \n> `{p}c-decline Wahha Selenskaya`",
			color = disnake.Colour.red()
				))

	if not clans.find_one({"name": name}):
		return await ctx.send(embed = disnake.Embed(
			title=":x: Возникла ошибка :x:",
			description="Клана с таким названием не существует! ",
			color = disnake.Colour.red()))

	invite_arr = invites.find_one({"name": name})
	if clans.find_one({"name": name})["owner"] == ctx.author.id:
		if nik in invite_arr['invites']:
			await ctx.send(embed = disnake.Embed(
			title=":white_check_mark: Все прошло успешно :white_check_mark:",
			description=f"Вы успешно отклонили заявку **{nik}**!",
			color = disnake.Colour.green()
				))
			invite_arr['invites'].remove(nik)
			invites.update_one({"name": name}, {"$set":{"invites": invite_arr['invites']}})

		else: 
			return await ctx.send(embed = disnake.Embed(
				title=f":x: Возникла ошибка :x:",
				description=f"Вы не можете отклонить заявку **{nik}**!",
				color = disnake.Colour.red()))
			
	
	else: 
			return await ctx.send(embed = disnake.Embed(
				title=f":x: Возникла ошибка :x:",
				description=f"Вы не можете отклонить заявку **{nik}**!",
				color = disnake.Colour.red()))
			


bot.run(con.BOT_TOKEN)