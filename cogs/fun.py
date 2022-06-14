from discord.ext import commands
import discord, logging, random

logger = logging.getLogger("Fun")

info = logger.info


class Fun(commands.Cog):
	def __init__(self, bot):
		info("Loading fun cog...")
		self.bot = bot
		info("Done!")

	@commands.command()
	async def scan(self, ctx, target="furry"):
		info("Called command fun")
		info("Checking target...")
		if target == 'furry':
			info("Target is furry.")
			await ctx.send("Сканирование сервера на наличие фуррей...")
			furrycount = 0
			furries = []
			for i in ctx.guild.members:
				if "furry" in i.name:
					info(f"Detected furry: {i.name}")
					info(f"ID: {i.id}")
					furrycount += 1
					furries.append({'name': i.name, 'id': i.id})
				else:
					info(f'User "{i.name}" Not furry!')
			await ctx.send(f"Сканирование завершено, Результат:\nОбнаружено фуррей: {furrycount}")

	@commands.command(aliases=['вопрос'])
	async def question(self, ctx, *, idk=None):
		response = random.choice(['да', 'нет', '50/50', 'я не знаю', 'idk'])
		await ctx.send(response)

async def setup(bot):
	await bot.add_cog(Fun(bot))