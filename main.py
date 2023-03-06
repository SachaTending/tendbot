print("Tendhost bot v1.1.3 is starting now...")
import discord
from discord.ext import commands
print("Loaded discord.py")
import loguru
print("Loaded loguru")
#import requests
#import cogs
import json
print("Loaded json")
import os
print("Loaded os")
import sys
print("Loaded sys")
import asyncio
import datetime, time 
print("Loaded asyncio")
import signal
print("Loaded signal")

from loguru_logging_intercept import setup_loguru_logging_intercept

setup_loguru_logging_intercept(modules="discord")
print("Patched discord to use loguru as default logger.")
command_executed_at_run = 0
#import logging_color
#logging_color.monkey_patch()
#print("Pacthed logging for colored output")
#from numba import jit

sys.path.append("modules")

RESTORE_MODE = False

logging = loguru.logger
logger = loguru.logger
__name__ = "BotMain"
logger.remove()
logger.add(sys.stdout, colorize=True, format="[{time:DD-MMM-YYYY}][{time:HH:mm:ss}]<lvl>[{name}][{level}] {message} </lvl>")
logger.info("It's loguru!")


#logging.configure(level=logging.INFO, format="[%(asctime)s] - [%(levelname)s] - [%(name)s(%(filename)s)]: %(message)s", datefmt="%H:%M:%S")
#logging.configure(format="[%(asctime)s] - [%(levelname)s] - [%(name)s(%(filename)s)]: %(message)s", datefmt="%H:%M:%S")

#logger = logging.getLogger("MainBot")
logger = logging

debug = logger.debug
info = logger.info
warn = logger.warning
error = logger.error
success = logger.success

info("Testing loguru...")
debug("This is debug")
info("This is info")
warn("This is warning")
error("This is error")
success("This is success")

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
	if ctx.author.id == 773136208439803934 or ctx.author.id == 775749058119204884 or 892823120283594804 == ctx.author.id or ctx.author.id == 483833827563798552:
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
		global startTime
		await bot.wait_until_ready()
		await bot.tree.sync()  # If you want to define specific guilds, pass a discord object with id (Currently, this is global)
		success('Sucessfully synced applications commands')
		success(f'Connected as {bot.user}')
		startTime = time.time()
	async def setup_hook(self):
		for filename in os.listdir("./cogs"):
			if filename.endswith(".py") and filename != "AMOGUS.py":
				try:
					await bot.load_extension(f"cogs.{filename[:-3]}")
					success(f"Loaded {filename}")
				except Exception as e:
					error(f"Failed to load {filename}")
					error(f"{e}")

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
async def on_message(msg: discord.Message):
	if msg.content.startswith("||"):
		return 0 # Ignore spoilers
	else:
		if msg.content.startswith("|"):
			ctx = bot.get_context(msg)
			await bot.invoke(msg)
			command_executed_at_run += 1


async def on_command_error(ctx, err):
	e = discord.Embed(color=0xff0000, title="Ошибка!")
	logger.error("Error!")
	try: 
		info(dir(err))
		info(dir(err.original))
		info(err.original.with_traceback)
	except: pass
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

@bot.event
async def on_ready(*argv):
	s = "Бот запущен"
	if RESTORE_MODE: 
		s += " в режиме восстановления\nПросьба не использовать бота во время восстановления."
		await bot.change_presence(status=discord.Status.idle, activity=discord.Game("Bot in restore mode, please do not use bot"))
	#await bot.get_channel(1026046100949442600).send("Бот запушен")
	await bot.get_channel(1026046100949442600).send(s)

async def on_shutdown(*argv):
	logger.info("Bot goes to shutdown!")
	await bot.get_channel(1026046100949442600).send("Бот остановлен")
	#sys.exit(0)

def on_shutdown2(*argv):
	try:
		loop = asyncio.get_running_loop()
	except RuntimeError:  # 'RuntimeError: There is no current event loop...'
		loop = None
	asyncio.run_coroutine_threadsafe(on_shutdown(*argv), loop)

#signal.signal(signal.SIGCHLD, on_shutdown2)
signal.signal(signal.SIGTERM, on_shutdown2)
signal.signal(signal.SIGALRM, on_shutdown2)
signal.signal(signal.SIGHUP, on_shutdown2)

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

@bot.command()
async def uptime(ctx):
	uptime = str(datetime.timedelta(seconds=int(round(time.time()-startTime))))
	await ctx.send(uptime)

@bot.command()
async def stat(ctx: commands.Context):
	uptime = str(datetime.timedelta(seconds=int(round(time.time()-startTime))))
	stat_info = f"```\nUptime: {uptime}"
	stat_info += f"\nExecuted commands(collected by on_message event): {command_executed_at_run}```"
	await ctx.send(stat_info)

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
