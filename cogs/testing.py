import discord
from discord.ext import commands
from discord import app_commands
import loguru, bundles, traceback

__name__ = "Testing"

logger = loguru.logger


class Testing(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.bundle = bundles.Bundle()
		@bot.tree.command()
		@app_commands.describe(
		    first_value='The first value you want to add something to',
		    second_value='The value you want to add to the first value',
		)
		async def add(interaction: discord.Interaction, first_value: int, second_value: int):
		    """Adds two numbers together."""
		    await interaction.response.send_message(f'{first_value} + {second_value} = {first_value + second_value}')
		logger.success("Done!")

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
	logger.info("Syncing command tree...")
	await bot.tree.sync()
	logger.success("Done!")