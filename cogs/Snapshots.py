from discord.ext import commands
import discord
import logging

logger = logging.getLogger("Snapshots")

debug = logger.debug
info = logger.info
warn = logger.warning
error = logger.error

class Snapshots(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def stest(self, ctx): 
		temp_snapshot = {"categories": {}}
		a = ""
		for i in ctx.guild.channels:
			if str(i.type) == 'category':
				a = str(i.name)
				temp_snapshot["categories"][a] = []
			elif str(i.type) == "text":
				temp_snapshot["categories"][a].append(str(i.name))

		info(temp_snapshot)


async def setup(bot):
	await bot.add_cog(Snapshots(bot))