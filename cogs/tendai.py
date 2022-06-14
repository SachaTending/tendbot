from discord.ext import commands
import logging
import json
import random
import time
import asyncio

logger = logging.getLogger("TendAi")

debug = logger.debug
info = logger.info
warn = logger.warning
error = logger.error

class TendAi(commands.Cog):
	def __init__(self, bot):
		info("Tendai loading now...")
		self.bot = bot
		info("Done!")
	async def experemental_func(self, ctx):
		await ctx.send("!!! Внимание !!!\n!!! Это эксперементальная функция !!!\nВсе ошибки присылайте ему TendingStream73#5806")
	@commands.command()
	async def tendai(self, ctx, arg1="", *, arg2=""):
		if arg1 == "stat":
			await self.experemental_func(ctx)
			data = json.load(open("tendai.words.json"))
			await ctx.send("Статистика:")
			await ctx.send(f"Предложений в базе данных: {len(data)}")
		elif arg1 == "info":
			await ctx.send("TendAi версия 1.0.1.1\nАвтор идеи(он же создатель DSBC Standard/Custom/Neuronic)Izzy8799#8179\nИдея взята с DSBC\nЕсли есть какие то ошибки, или вы хотите связатся с автором TendAi: TendingStream73#5806")
		else:
			info("event.reply called!")
			data = json.load(open("tendai.words.json"))
			random_msg = random.choice(data)
			async with ctx.typing():
				await asyncio.sleep(2)
			await ctx.reply(random_msg)

	@commands.Cog.listener()
	async def on_message(self, message):
		info("New message!")
		try: info(f"Server: {message.guild.name}")
		except: pass
		try: info(f"Channel: {message.channel.name}")
		except: pass
		info(f"User: {message.author.name}")
		info(f"Message: {message.content}")
		info(f"Attachements: {message.attachments}")
		info("Embeds:")
		embeds = message.embeds # return list of embeds
		for embed in embeds: info(embed.to_dict()) # it's content of embed in dict
		if message.content.startswith("|"):
			info("Ignore.")
			return 0
		else:
			try:
				if random.randint(0,5) == 5:
					if message.guild.id == 963381813139624056:
						info("Message in DSBC")
						info("Checking for channel...")
						if message.channel.id == 973916297454829618 and message.author.id != 934851107870621726:
							info("This is allowed channel!, replying...")
							data = json.load(open("tendai.words.json"))
							random_msg = random.choice(data)
							async with message.channel.typing():
								await asyncio.sleep(2)
							await message.channel.send(random_msg, reference=message)
						else:
							info("This is not allowed channel or author self bot!")
				else:
					if message.guild.id == 963381813139624056:
						info("Message in DSBC")
						info("Checking for channel...")
						if message.channel.id == 973916297454829618 and message.author.id != 934851107870621726:
							info("Saving...")
							data = json.load(open("tendai.words.json"))
							if message.content in data:
								info("Word already in database!")
								return 0
							data.append(message.content)
							json.dump(data, open("tendai.words.json", "w"))
							info("Reacting...")
							await message.add_reaction("🍪")
							info("Done!")
			except Exception as e:
				info("Error!")
				info(e)


async def setup(bot):
	info("Setup of TendAi called!")
	await bot.add_cog(TendAi(bot))