from flask import Flask, request, url_for, redirect
import logging, threading, discord, random, string, ConfMan
from discord.ext import commands
import multiprocessing as mp
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized

logger = logging.getLogger("Api server")

info = logger.info
#info = lambda msg: print(f"Api server: {msg}")

app = Flask("Api server")

class API_Server(commands.Cog):
	def __init__(self, bot):
		global app
		global app_thread
		info("Initializating database...")
		self.db = ConfMan.DB("API.API_DB.json")
		info("Initializating base server...")
		self.app = app
		info("Setting vars...")
		self.bot = bot
		self.app.config["DISCORD_CLIENT_ID"] = 934851107870621726
		self.app.config["DISCORD_CLIENT_SECRET"] = "tJUw-22OEwm7LhSFnAHwGWTiIuq6fFol"
		self.app.config["DISCORD_REDIRECT_URI"] = "/tendbotapi"
		self.app.config["DISCORD_BOT_TOKEN"] = ""
		self.characters = string.ascii_letters + string.digits
		info("Starting server process...")
		self.app_thread = mp.Process(target=lambda: self.app.run(host="0.0.0.0", port=7579))
		self.app_thread.start()
		app_thread = self.app_thread

	@app.route("/login/")
	def login():
		return discord.create_session()

	@app.errorhandler(Unauthorized)
	def redirect_unauthorized(e):
		return redirect(url_for("login"))

	@app.route("/<api_request>")
	def handlerequest(api_request):
		info(f"Requested api command: {api_request}")
		info("Trying to find api command...")
		for i in bot.cogs:
			info(f"Target cog: {i}")
			cog = bot.cogs[i]
			if hasattr(cog, "API_methods"):
				info(f"Cog {i} has api methods!")
				if hasattr(cog.API_methods, api_request):
					info(f"And has api method {api_request}!")
					info("Executing api method...")
					out = getattr(cog.API_methods, api_request)()
					info(f"API method output: {out}")
					return out
				else:
					info("But dont have target api method")
			else:
				info(f"Target cog does api support")
		info("Api method not founded, returning error code")
		return {"return": {"code": 404, "message": "api method not found"}}
	@app.route("/tendbotapi/<api_request>")
	def hr(api_request):
		info(f"Requested api command: {api_request}")
		info("Trying to find api command...")
		for i in bot.cogs:
			info(f"Target cog: {i}")
			cog = bot.cogs[i]
			if hasattr(cog, "API_methods"):
				info(f"Cog {i} has api methods!")
				if hasattr(cog.API_methods, api_request):
					info(f"And has api method {api_request}!")
					info("Executing api method...")
					out = getattr(cog.API_methods, api_request)()
					info(f"API method output: {out}")
					return out
				else:
					info("But dont have target api method")
			else:
				info(f"Target cog does api support")
		info("Api method not founded, returning error code")
		return {"return": {"code": 404, "message": "api method not found"}}
	@app.route("/tendbotapi")
	def gendoc():
		info("Generating documentation...")
		docpage = "<!DOCUMENT_HTML>\n<title>TendBotAPI Documentation</title>\n<h1>Welcome to tendbot api documentation!</h1>\n"
		for i in bot.cogs:
			info(f"Target cog: {i}")
			cog = bot.cogs[i]
			if hasattr(cog, "API_methods"):
				info(f"Cog {i} has api methods!")
				if hasattr(cog.API_methods, "gendochtmlamogus"):
					info("And has api documentation!")
					docpage += f"<h1>{i}:</h1>\n"
					docpage += getattr(cog.API_methods, "gendochtmlamogus")()
				else:
					info("But dont have api documentation")
			else:
				info(f"Target cog does api support")
		return docpage

	@commands.command()
	async def apitoken(self, ctx):
		if self.db.get(ctx.author.id) != None:
			token = self.db.get(ctx.author.id)
			await ctx.send("Your api token sended to dm")
			await ctx.author.send(f"Your tendbotapi token: {token}")
		else:
			await ctx.send("Please wait, your token generating now...")
			token = ""
			while True:
				for i in range(64): token += random.choice(list(self.characters))
				if self.db.search(token) != None: pass
				else: break
			self.db.set(ctx.author.id, token)
			await ctx.send("Your api token sended to dm")
			await ctx.author.send(f"Your tendbotapi token: {token}")

async def setup(bota):
	global bot
	bot = bota
	await bota.add_cog(API_Server(bota))

async def teardown(bot):
	info("Stopping server...")
	app_thread.terminate()
	info("Server stopped!")