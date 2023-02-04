import discord
from discord.ext import commands
import logging
import requests
import json
import aiohttp
import random
import os
import time
from rule34Py import rule34Py

r34Py = rule34Py()

logger = logging.getLogger("NSFW")

info = logger.info

intents = discord.Intents.default()

client = discord.Client(intents=intents)

def _fetcher(count):
	#images = []
	embeds = []
	for i in range(0, count):
		info("Fetching image url from nekos.life...")
		r = requests.get("https://nekos.life/api/v2/img/lewd")
		rjson = json.loads(r.text)
		url = rjson["url"]
		info(f"URL: {url}")
		#images.append(url)
		#info("Creating embed...")
		#e = discord.Embed()
		#e.set_image(url=url)
		embeds.append(url)
	return embeds

class Nsfw(commands.Cog):
	def __init__(self, bot):
		info("Nsfw cog loading now...")
		self.bot = bot
		self.rule34 = rule34Py()
		info("Done!")

	def calculate_posts(self, posts):
		posts_new = []
		for i in posts:
			for a in i:
				posts_new.append(a)
		return posts_new
	def justafunc(self, what: int):
		return what // 1000
	def create_tags_str(self,tags,url):
		if True:
			print("Skip")
			return tags
		else:
			if len(str(tags)) < 256:
				tags_text = ""
				for i in tags:
					tags_text += i + ", "
				return tags_text
			else:
				info(len(tags))
				tags_cuted = ""
				for i in tags:
					tags_cuted += i + ", "
				info(len(tags_cuted))
				lengh = 2000-len(url)
				if len(tags_cuted) >= lengh:
					tags_2000 = ""
					for i in range(0,2000-len(url)):
						tags_2000 += tags_cuted[i]
					return tags_2000

	@commands.command(brief="По переводу комманды понятно")
	@commands.is_nsfw()
	async def lewd(self, ctx, count=1):
		if count > 50:
			raise RuntimeError("чел, а зачем?")
		count = int(count)
		#images = _fetcher(count)
		#embeds = []
		text = ""
		embeds = _fetcher(count)
		for i in embeds:
			info("Sending...")
			#await ctx.send(embed=i)
			#await ctx.send(i)
			#text += i + "\n"
			await ctx.send(i)
		#await ctx.send(text)
		info("Done!")

	@commands.command(brief="Найти nsfw по тэгам")
	@commands.is_nsfw()
	async def r34(self, ctx, r34tags="random", count=50, page_id=None):
		#if ctx.author.id == 775749058119204884:
		#	raise RuntimeError("ERROR")
		embeds = []		
		count = int(count)
		r34tags = str(r34tags)
		info(f"rule34 tags: {r34tags}")
		blocked_tags_list = []
		posts = await self.rule34.search(tags=(r34tags.split(" ")), limit=count,page_id=page_id) 
		blocked_tags = 0
		if posts != []:
			for i in posts:
				skip = False
				info(len(r34tags))
				tags = self.create_tags_str(i.tags,i.url)
				info(len(tags))
				tags_text = ""
				info("Creating embed...")
				#lengh = 2000-len(i.url)
				if True:
					#logging.warn("Lengh of tegs over 2000!")
					#logging.warn(tags)
					#logging.warn(len(tags))
					#logging.warn("Skipping...")
					skip = False
				else:
					#tags_text = f"Tags:{tags}" + "\n" + i.url
					pass
				if "furry" in i.tags or "younger_futanari" in i.tags or "futurani" in i.tags or "my_little_pony" in i.tags or "yaoi" in i.tags or "animal_penis" in i.tags or "fur" in i.tags or "cannibalism" in i.tags:
					blocked_tags += 1
					for tag in i.tags:
						if "furry" == tag or "younger_futanari" == tag or "futurani" == tag or "my_little_pony" == tag or "yaoi" == tag or "animal_penis" == tag or "fur" == tag or "cannibalism" == tag:
							if tag in blocked_tags_list:
								pass
							else:
								blocked_tags_list.append(tag)
					info("Founded blocked tag!, Skipping...")
					skip = True
				#e.set_image(url=i.url)
				info(f"URL: {i.url}")
				if skip == False:
					file_name = 0
					info(f"Founded tags: {i.tags}")
					if i.url.endswith(".mp4"):
						#tags_text = f"Tags: {tags}" + "\nSource: " + i.source + "\n" + i.url
						#tags_text = f"Tags: {tags}"
						#file_name += 1
						#os.system(f'ffmpeg -i {i.url} -filter_complex "fps=10,scale=-1:640,crop=ih:ih,setsar=1,palettegen" /tmp/{file_name}.png')
						#os.system(f'ffmpeg -i {i.url} -i /tmp/{file_name}.png -filter_complex "[0]fps=10,scale=-1:640,crop=ih:ih,setsar=1[x];[x][1:v]paletteuse" /tmp/{file_name}.gif')
						#os.remove(f"/tmp/{file_name}.png")
						#embeds.append({"tags_text": tags_text, "embed": tags_text, "file": None})
						pass
					tags_text = f"Tags: {tags}" + "\nSource: " + i.source + "\n" + i.url
					#print(i.tags)
					embeds.append({"tags_text": tags_text, "embed": tags_text, "file": None})
				elif skip == True:
					info("Skipped.")
		else:
			await ctx.send("Ничего не найдено!")
		sended = 0
		for i in embeds:
			embed = i["embed"]
			tags = i["tags_text"]
			if i["file"] == None:
				try:
					await ctx.send(tags)
					sended += 1
				except:
					pass
			else:
				await ctx.send(tags, file=file)
			#await ctx.send(embed=embed)
			#time.sleep(1)
			#os.remove(file)
		await ctx.send(f"Было найдено: {sended}")
		if blocked_tags == 0:
			pass
		else:
			await ctx.send(f"Заблокированы тэги: {blocked_tags_list}")
			await ctx.send(f"Количество заблокированых тэгов: {blocked_tags}")
			count2 = sended
			count2 += blocked_tags
			await ctx.send(f"В сумме(найдено и заблокировано): {count2}")
		info("Done!")
	@commands.command(brief="Подсчитать количество nsfw по тэгу")
	async def r34count(self, ctx, r34tags="random", count=2000):
		#if ctx.author.id == 775749058119204884:
		#	raise RuntimeError("ERROR")
		embeds = []		
		count = int(count)
		r34tags = str(r34tags)
		info(f"rule34 tags: {r34tags}")
		page_id = random.randint(1,1000)
		blocked_tags_list = []
		posts = []
		await ctx.send("Поиск...")
		if count > 1000:
			for i in range(1,int(self.justafunc(count))):
				posts.append(await self.rule34.search(tags=(r34tags.split(" ")), limit=1000,page_id=i))
			old_posts = posts
			posts = self.calculate_posts(posts)
		blocked_tags = 0
		count2 = 0
		if posts != []:
			await ctx.send("Подсчёт...")
			for i in posts:
				skip = False
				info(len(r34tags))
				tags = self.create_tags_str(i.tags,i.url)
				info(len(tags))
				tags_text = ""
				info("Creating embed...")
				#lengh = 2000-len(i.url)
				if True:
					#logging.warn("Lengh of tegs over 2000!")
					#logging.warn(tags)
					#logging.warn(len(tags))
					#logging.warn("Skipping...")
					skip = False
				else:
					#tags_text = f"Tags:{tags}" + "\n" + i.url
					pass
				if "furry" in i.tags or "younger_futanari" in i.tags or "futurani" in i.tags or "my_little_pony" in i.tags or "yaoi" in i.tags or "animal_penis" in i.tags or "fur" in i.tags or "cannibalism" in i.tags:
					blocked_tags += 1
					for tag in i.tags:
						if "furry" == tag or "younger_futanari" == tag or "futurani" == tag or "my_little_pony" == tag or "yaoi" == tag or "animal_penis" == tag or "fur" == tag or "cannibalism" == tag:
							if tag in blocked_tags_list:
								pass
							else:
								blocked_tags_list.append(tag)
					info("Founded blocked tag!, Skipping...")
					skip = True
				#e.set_image(url=i.url)
				info(f"URL: {i.url}")
				if skip == False:
					file_name = 0
					info(f"Founded tags: {i.tags}")
					count2 += 1
					#print(i.tags)
					#embeds.append({"tags_text": tags_text, "embed": tags_text, "file": None})
				elif skip == True:
					info("Skipped.")
		else:
			await ctx.send("Ничего не найдено!")
		await ctx.send(f"Было найдено: {count2}")
		if blocked_tags == 0:
			pass
		else:
			await ctx.send(f"Заблокированы тэги: {blocked_tags_list}")
			await ctx.send(f"Количество заблокированых тэгов: {blocked_tags}")
			count2 += blocked_tags
			await ctx.send(f"В сумме(найдено и заблокировано): {count2}")
		info("Done!")
class rule34Py():
	def __init__(self):
		#self.url = "https://r34-json-api.herokuapp.com/posts"
		#self.client = aiohttp.ClientSession()
		pass

	async def search(self, tags = None, page_id = None, limit = 1000):
		params = {
			"limit": limit
		}
		if tags:
			params["tags"] = "+".join(tags),
		if page_id:
			params["page_id"] = str(page_id)
		
		response = []
		#async with self.client.get(self.url, params = params) as session:
		#	response = await session.json()
		response = r34Py.search(tags=params.get("tags"), page_id=params.get("page_id", 1), limit=limit)
		
		posts = []

		for post in response:
			"""
			url = post["file_url"]
			source = post.get("source", None)
			id = post["id"]
			size = [post["width"], post["height"]]
			creator_id = post["creator_id"]
			_tags = post["tags"]
			"""

			posts.append(Post(response.id, response.image, "none", response.tags, response.size, 0))

		return posts

class Post:
	def __init__(self, id, url, source, tags, size, creator_id):
		self.id = id
		self.size = size
		self.source = source
		self.url = url
		self.creator_id = creator_id
		self.tags = tags

async def setup(bot):
	print("Setup of nsfw cog called!")
	await bot.add_cog(Nsfw(bot))
