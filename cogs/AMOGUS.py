from discord.ext import commands
import logging
import random

logger = logging.getLogger("AMOGUS")

debug = logger.debug
info = logger.info
warn = logger.warning
error = logger.error

sus_words = ["sus", "amogus", "amongus", "imposter", "sussy"]

amogus_url = ["https://cdn.discordapp.com/attachments/958072912047378443/964603871261491211/video-235a310b2c60c243e1709624884f0d64-V.mp4", "https://c.tenor.com/ss49WMsRilQAAAAd/among-us-drip.gif", "https://c.tenor.com/P8KjYDcd7JwAAAAS/among-us-among-drip.gif"]

class Amogus(commands.Cog):
	def __init__(self, bot):
		info("Amogus cog loading now...")
		self.bot = bot
		info("Done!")

	@commands.Cog.listener()
	async def on_message(self, message):
		if message.content.lower() in sus_words and message.author.bot != True:
			info(f"User {message.author.name} requested AMOGUS.")
			await message.channel.send(random.choice(amogus_url), reference=message)

def setup(bot):
    info("Amogus cog setup called!")
    bot.add_cog(Amogus(bot))