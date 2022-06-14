from discord.ext import commands
import discord
import logging
import pydustry
import os
from ping3 import ping as ping_lib
import dns.resolver

logger = logging.getLogger("Utils")

debug = logger.debug
info = logger.info
warn = logger.warning
error = logger.error

class Utils(commands.Cog):
	def __init__(self, bot):
		info("Utils cog loading now")
		self.bot = bot
		self.resolver = dns.resolver.Resolver()
		self.resolver.nameservers = ['1.1.1.1']
		info("Done!")

	async def is_owner(ctx):
		info("Requested bot admin command! Checking...")
		if ctx.author.id == 773136208439803934 or ctx.author.id == 775749058119204884 or 892823120283594804 == ctx.author.id:
			info("This is admin/owner of the bot, can continue execution")
			return True
		else:
			info("This is not admin/owner of the bot!")
			info(f"Requester nickname:{ctx.message.author.name}")
			return False

	@commands.command()
	async def modules(self, ctx):
		cogscount = len(self.bot.cogs)
		cogsnames = []
		for i in self.bot.cogs: cogsnames.append(i)
		wtf = ""
		for i in self.bot.cogs: wtf += f"{i} "
		embed = discord.Embed(title="Модули", color=0x0080ff)
		embed.add_field(name="Количество загруженых модулей", value=cogscount, inline=True)
		embed.add_field(name="Название загруженых модулей", value=wtf)
		await ctx.send(embed=embed)

	@commands.command()
	async def members(self, ctx, wtf=""):
		embedVar = discord.Embed(title=f'На сервере {ctx.guild.member_count} {wtf}', color=0x0080ff)
		await ctx.send(embed=embedVar)
	@commands.command()
	async def status(self, ctx, ip="localhost", port: int=6567):
		print(1)
		embed = discord.Embed(title="Статус", color=0x0080ff)
		server = pydustry.Server(ip, port)
		status = server.get_status()
		info(status)
		embed.add_field(name="Игроков: ", value=str(status['players']))
		embed.add_field(name="Карта: ", value=status['map'])
		embed.add_field(name="Версия: ", value=str(status['version']))
		embed.add_field(name="Название сервера: ", value=status['name'])
		embed.add_field(name="Волна: ", value=str(status['wave']))
		await ctx.send(embed=embed)
	@commands.command()
	@commands.check(is_owner)
	async def clear_console(self, ctx):
		await ctx.send("Очистка консоли бота от мусора...")
		os.system("clear")
		os.system("cls")
		await ctx.send("Готово.")

	@commands.command()
	async def ping(self, ctx, host: str="discord.com"):
		try: ip = [i.to_text() for i in self.resolver.resolve(host, 'a')][0]
		except: ip = host
		e = discord.Embed(title="Pong!(результат в миллисекундах)", color=0x0080ff)	
		zeroping = ping_lib(host, unit='ms', size=0)
		default  = ping_lib(host, unit='ms', size=56)
		default2 = ping_lib(host, unit='ms', size=128)
		if ip != host: e.add_field(name='Хост: ', value=f"{ip}({host})")
		else: e.add_field(name='Хост: ', value=ip)
		e.add_field(name='Используя "нулевые пакеты": ', value=int(zeroping))
		e.add_field(name='Используя пакеты размером 56 байт: ', value=int(default))
		e.add_field(name='Используя пакеты размером 128 байт: ', value=int(default2))
		await ctx.send(embed=e)

async def setup(bot):
	info("Setup of utils cog called!")
	await bot.add_cog(Utils(bot))