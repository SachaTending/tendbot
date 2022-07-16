from discord.ext import commands
from flask import request
import discord
import logging
import pydustry
import os
from ping3 import ping as ping_lib
import dns.resolver
import sys, asyncio, traceback
import speech_recognition as sr
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
import ConfMan

logger = logging.getLogger("Utils")

debug = logger.debug
info = logger.info
warn = logger.warning
error = logger.error

class Utils(commands.Cog):
	def __init__(self, bota):
		info("Utils cog loading now")
		global bot
		global apidb
		self.apidb = ConfMan.DB("API.API_DB.json")
		apidb = self.apidb
		self.bot = bota
		bot = bota
		self.resolver = dns.resolver.Resolver()
		self.resolver.nameservers = ['1.1.1.1']
		info("Done!")

	class API_methods:
		def gendochtmlamogus():
			return "<p>utils_modules - returns loaded modules/возвращает загружене модули</p>\n<p>utils_mstatus?server=host_here&port=port_here - WARNING!!! This metod copied from MindToolKitAPI/Внимание!!! Первоисточником этого метода является MindToolKitAPI -returns mindustry server status/возвращает статус mindustry сервера"
		def utils_modules():
			cogsnames = []
			for i in bot.cogs: cogsnames.append(i.lower())
			return {"return": {"code": 200, "message": cogsnames}}
		def utils_mstatus():
			args = request.args
			needkeys = []
			out = {"return": {}}
			try: server = args["server"]
			except: needkeys.append("server - server address")
			try: port = args["port"]
			except: needkeys.append("port - server port")
			if needkeys == []:
				try:
					server = pydustry.Server(server, int(port))
					status = server.get_status()
					out["return"] = {"code": 200, "message": status}
				except Exception as e: out["return"] = {"code": 500, "message": str(e)}
			else:
				out["return"] = {"code": 500, "message": ("need options: " + ", ".join(needkeys))}
			return out
		def utils_tokeninfo():
			tendbotapitoken = request.headers.get("API_TOKEN")
			if tendbotapitoken != None:
				tokenid = apidb.search(tendbotapitoken)
				info(f"Token({tendbotapitoken}) id is {tokenid}")
				if tokenid != None:
					try: user = bot.get_user(tokenid)
					except: return {"return": {"code": 500, "message": "the user id specifed in token invalid"}}
					out = {
						"return": {
						"code": 200,
						"message": {
							"name": "",
							"id": 0,
							"avatar_url": ""
							}
						}
					}
					out["return"]["message"]["name"] = user.name
					out["return"]["message"]["id"] = user.id
					out["return"]["message"]["avatar_url"] = user.avatar
					return out
				else: 
					return {"return": {"code": 500, "message": "invalid token"}}
			else:
				return {"return": {"code": 500, "message": "pls specify token in API_TOKEN header"}}

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
	async def status(self, ctx, ip="localhost", port: int=7576):
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

	@commands.command(aliases=['avatar'])
	async def аватар(self, ctx, member='self'):
		if member == 'self': member = ctx.author
		else: member = self.bot.fetch_user(int(member))
		info(member.avatar_url)

	@commands.command(name="eval")
	@commands.is_owner()
	async def _eval(self, ctx, *, cmd="'hi'"): 
		out = eval(cmd)
		if out != None: await ctx.send(out)
	@commands.Cog.listener()
	async def on_command_error(self, ctx, err):
		e = discord.Embed(color=0xff0000, title="Ошибка!")
		logger.error("Error!")
		try: 
			info(err.original.with_traceback.__traceback__)
		except: pass

	@commands.command()
	async def recog(self, file="attach", lang="ru_RU"):
		await ctx.send("in dev/в разработке")


async def setup(bot):
	info("Setup of utils cog called!")
	await bot.add_cog(Utils(bot))