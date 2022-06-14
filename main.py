print("Tendhost bot v1.1.2 is starting now...")
import discord
from discord.ext import commands
print("Loaded discord.py")
import logging
print("Loaded logging")
#import requests
#import cogs
import json
print("Loaded json")
import os
print("Loaded os")
import sys
print("Loaded sys")
import asyncio
print("Loaded asyncio")
#from numba import jit

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] - [%(levelname)s] - [%(name)s(%(filename)s)]: %(message)s", datefmt="%H:%M:%S")

logger = logging.getLogger("MainBot")

debug = logger.debug
info = logger.info
warn = logger.warning
error = logger.error

info("Intializating vars...")

config = json.load(open("config.json"))
token = config["token"]
prefix = config["prefix"]
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
#bot = commands.Bot(command_prefix=prefix, intents=intents)

info("Intializating base commands...")

# diskord.py commands section start

async def is_owner(ctx):
	info(f"Requested bot admin command! Checking... {ctx.author.name}")
	if ctx.author.id == 773136208439803934 or ctx.author.id == 775749058119204884 or 892823120283594804 == ctx.author.id:
		info("This is admin/owner of the bot, can continue execution")
		return True
	else:
		info("This is not admin/owner of the bot!")
		info(f"Requester nickname:{ctx.message.author.name}")
		return False

#@bot.user_command()
#async def slap(ctx, user):
#	await ctx.respond(f'{ctx.author.name} дал лещя {user.name}')
class Bot(commands.Bot):
	def __init__(self, intents):
		super().__init__(command_prefix=prefix, intents=intents)
	async def startup(self):
		await bot.wait_until_ready()
		await bot.tree.sync()  # If you want to define specific guilds, pass a discord object with id (Currently, this is global)
		info('Sucessfully synced applications commands')
		info(f'Connected as {bot.user}')
	async def setup_hook(self):
		for filename in os.listdir("./cogs"):
			if filename.endswith(".py") and filename != "AMOGUS.py":
				try:
					await bot.load_extension(f"cogs.{filename[:-3]}")
					info(f"Loaded {filename}")
				except Exception as e:
					logger.error(f"Failed to load {filename}")
					logger.error(f"{e}")

		self.loop.create_task(self.startup())

bot = Bot(intents=intents)

@bot.command()
@commands.check(is_owner)
async def error(ctx):
	raise RuntimeError("Hello, world!")

@bot.command()
@commands.check(is_owner)
async def shutdown(ctx):
	if ctx.author.id != 773136208439803934:
		raise RuntimeError("нет")
	await ctx.send("Выключение...")
	sys.exit(0)

@bot.event
async def on_command_error(ctx, err):
	e = discord.Embed(color=0xff0000, title="Ошибка!")
	logger.error("Error!")
	try:
		for i in err:
			info(i)
	except:
		info(err)
	e.add_field(name="Traceback most recent call", value="***костыль чтобы работало***", inline=False)
	try:
		for i in err:
			e.add_field(name=f"***костыль чтобы работало***", value=str(i), inline=True)
	except Exception as er:
		print(er)
		e.add_field(name=f"***костыль чтобы работало***", value=str(err), inline=False)
	await ctx.send(embed=e)

@bot.command()
@commands.check(is_owner)
async def reload_cog(ctx, cog):
	#bot.unload_extension(cog)
	#bot.load_extension(cog)
	await bot.reload_extension(cog)
@bot.command()
@commands.check(is_owner)
async def unload_cog(ctx, cog):
	await bot.unload_extension(cog)

@bot.command()
@commands.check(is_owner)
async def load_cog(ctx, cog):
	await bot.load_extension(cog)

# diskord.py commands section end

info("Intializating cogs...")

# diskord.py cogs section
async def load_all_cogs():
	await bot.load_extension("cogs.nsfw")
	await bot.load_extension("cogs.economy")
	# bot.load_extension("cogs.AMOGUS")
	await bot.load_extension("cogs.utils")
	await bot.load_extension("cogs.tendai")
# diskord.py cogs section

#asyncio.run(load_all_cogs())

info("Starting bot...")
#@jit()
def start():
	bot.run(token)

start()
