import discord
from discord.ext import commands
import loguru, bundles, traceback

__name__ = "Testing"

logger = loguru.logger

class Testing(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.bundle = bundles.Bundle()
		logger.info("Done!")

	@commands.command()
	@commands.is_owner()
	async def bundle_get(self, ctx, target):
		try:
			await ctx.send(self.bundle.get(ctx.guild.id, target))
		except:
			await ctx.send("```\n" + traceback.format_exc() + "\n```")

async def setup(bot):
	logger.info("Loading...")
	await bot.add_cog(Testing(bot))