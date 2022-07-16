import logging
from discord.ext import commands
import discord

logger = logging.getLogger("Actions Logger")

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] - [%(levelname)s] - [%(name)s(%(filename)s)]: %(message)s", datefmt="%H:%M:%S")


info = logger.info

class ActionsLogger(commands.Cog):
	def __init__(self, bot):
		info("Loading Actions logger...")
		self.bot = bot
		info("Done!")

	@commands.command(aliases=["al"])
	async def actionslogger(self, ctx, action="info", param1=None, param2=None, param3=None):
		if action == "info":
			await ctx.send("Модуль ActionsLogger версия 1.0\nРазработан для бота Tendbot\nРазработкой занимался TendingStream73#5806")
		elif action == "channels":
			channels_txt = "Все каналы этого сервера:\n"
			for channel in ctx.guild.channels:
				channels_txt += f"{channel.name}\n"
			await ctx.send(channels_txt)

	@commands.Cog.listener()
	async def on_message_edit(self, message_before, message_after):
		info(f"User {message_before.author.name} edited a message in server {message_before.guild.name}, channel {message_before.channel.name}: {message_before.content} -> {message_after.content}")
		if message_before.guild.id == 934457765768867850 and message_before.content != message_after.content:
			embed = discord.Embed(color=0x0080ff, title=f"Пользователь {message_before.author.name} отредактировал сообщение!")
			embed.add_field(name="Канал", value=f"#{message_before.channel.name}", inline=False)
			embed.add_field(name="Было", value=message_before.content, inline=False)
			embed.add_field(name="Стало", value=message_after.content, inline=False)
			i = self.bot.get_channel(992121883174654023)
			await i.send(embed=embed)
	
	@commands.Cog.listener()
	async def on_message_delete(self, message):
		info(f"User {message.author.name} deleted a message on server {message.guild.name}, channel {message.channel.name}: {message.content}")
		if message.guild.id == 934457765768867850:
			embed = discord.Embed(color=0x0080ff, title=f"Пользователь {message.author.name} удалил сообщение в канале #{message.channel.name}")
			embed.add_field(name="Сообщение", value=message.content, inline=False)
			channel = self.bot.get_channel(992121797669564558)
			await channel.send(embed=embed)


async def setup(bot):
	await bot.add_cog(ActionsLogger(bot))