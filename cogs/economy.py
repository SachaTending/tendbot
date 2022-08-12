import random
from discord.ext import commands
import logging
import os
import json
import time

logger = logging.getLogger("Economy")

debug = logger.debug
info = logger.info
warn = logger.warning
error = logger.error

cooldown = {}

class Economy(commands.Cog):
    def __init__(self, bot, cooldown):
        info("Economy cog loading now...")
        self.bot = bot
        self.somefuncs = somefuncs
        self.cooldown = cooldown
        info("Done!")

    async def is_owner(ctx):
        info("Requested bot admin command! Checking...")
        if ctx.author.id in [773136208439803934, 775749058119204884, 892823120283594804]:
            info("This is admin/owner of the bot, can continue execution")
            return True
        else:
            info("This is not admin/owner of the bot!")
            info(f"Requester nickname:{ctx.message.author.name}")
            return False

    def iscooldown(self, userid):
        if userid in cooldown:
            usercooldown = self.cooldown[userid]
            currenttime = time.time()
            out = currenttime - usercooldown
            if out < 60:
                return int(out)
            else:
                self.cooldown[userid] = time.time()
                return 0
        else:
            self.cooldown[userid] = time.time()
            return 0
    @commands.command(brief="Казино")
    async def casino(self, ctx, something: int, count: int=1):
        usercooldown = self.iscooldown(ctx.author.id)
        if usercooldown == 0:
            # count = int(count)
            maximum = 2000
            if count != 1:
                if count <= maximum:
                    msg = await ctx.reply(f"Хмм, ну ладно, ставка на {something} {count} раз")
                    #await ctx.send(f"{something} Говоришь?")
                    wins = 0
                    fails = 0
                    wtf = 0
                    for i in range(1,count):
                        something2 = random.randint(1, 2)
                        if something2 == something:
                            wins += 1
                            #await ctx.send("Ты выиграл!")
                            keydata = self.somefuncs.getkey(str(ctx.author.id))
                            balance = keydata["balance"] + 10.0
                            keydata["balance"] = balance
                            self.somefuncs.dumpkey(str(ctx.author.id), keydata)
                            wtf += 10
                        #await ctx.send("На ваш баланс было зачислено 10 флопских коинов")
                        else:
                            fails += 1
                            wtf -= 10
                            #await ctx.send("Ты проиграл!")
                            #await ctx.send(f"Ответ: {something2}")
                    await msg.edit(content=f"Выигрышей: {wins}\nПроигрышей: {fails}\nЗачислено: {wtf}")
                    #await ctx.send(f"Проигрышей: {fails}")
                    #await ctx.send(f"Зачислено: {wtf}")
                else:
                    await ctx.reply(f"Слишком много!\nМаксимум {maximum}")
            else:
                msg = await ctx.reply(f"{something} Говоришь?")
                for i in range(1, 100):
                    something2 = random.randint(1, 2)
                if something2 == something:
                    await msg.edit(content="Ты выиграл!")
                    keydata = self.somefuncs.getkey(str(ctx.author.id))
                    balance = keydata["balance"] + 10.0
                    keydata["balance"] = balance
                    self.somefuncs.dumpkey(str(ctx.author.id), keydata)
                    await msg.edit(content="На ваш баланс было зачислено 10 флопских коинов")
                else:
                    await msg.edit(content=f"""
Ты проиграл!
Ответ: {something2}
С вашего баланса было снято 10 флопских коинов
""")
                    keydata = self.somefuncs.getkey(str(ctx.author.id))
                    balance = keydata["balance"] - 10.0
                    keydata["balance"] = balance
                    self.somefuncs.dumpkey(str(ctx.author.id), keydata)
        else:
            raise RuntimeError(f"Кулдаун! {usercooldown}")
    @commands.command(aliases=["b", "mb"], brief="Проверить баланс+регистрация в дб")
    async def mybalance(self, ctx):
        #await ctx.send(self.somefuncs.getdb())
        if str(ctx.author.id) in self.somefuncs.getdb():
            pass
        else:
            #await ctx.send("Вы не зарегестрированы в базе данных.")
            self.somefuncs.regdb(str(ctx.author.id))
        data = self.somefuncs.getkey(str(ctx.author.id))
        balance = data["balance"]
        await ctx.send(f"Ваш баланс: {balance} флопских коинов.")
    @commands.command()
    @commands.check(is_owner)
    async def setbalance(self, ctx, balance: float):
        keydata = self.somefuncs.getkey(str(ctx.author.id))
        keydata["balance"] = balance
        self.somefuncs.dumpkey(str(ctx.author.id), keydata)
        await self.mybalance(ctx)
    @commands.command()
    async def transfer(self, ctx, money: float, destiation):
        final_username = str(destiation.translate({ ord(c): None for c in "<@>" }))
        if str(final_username) in self.somefuncs.getdb():
            pass
        else:
            #await ctx.send("Вы не зарегестрированы в базе данных.")
            self.somefuncs.regdb(str(final_username))

        if self.somefuncs.getmoney(str(ctx.author.id)) >= money:
            info("Денег достаточно для перевода, обновление информации в базе данных...")
            info(1)
            currnetmoney = self.somefuncs.getmoney(str(ctx.author.id))
            info(2)
            currnetmoney -= float(money)
            info(3)
            self.somefuncs.setmoney(final_username, self.somefuncs.getmoney(final_username)+money)
            info(4)
            self.somefuncs.setmoney(str(ctx.author.id), currnetmoney)
            info(5)
            await ctx.send(f"Ваш баланс: {currnetmoney}")
            info(6)
            info("готово.")


class somefuncs:
    def getkey(key):
        db = somefuncs.getdb()
        return db[key]
    def getdb():
        return json.load(open("db.economy.json"))
    def regdb(userid: str):
        db = somefuncs.getdb()
        db[userid] = {"balance": 50.0}
        json.dump(db, open("db.economy.json", "w"))
    def dumpkey(key, data):
        dbout = somefuncs.getdb()
        dbout[key] = data
        somefuncs.dumpdb(dbout)
    def dumpdb(data):
        json.dump(data, open("db.economy.json", "w"))
    def getmoney(userid: str):
        return somefuncs.getkey(userid)["balance"]
    def setmoney(userid: str, money: float):
        db = somefuncs.getkey(userid)
        db["balance"] = money
        somefuncs.dumpkey(userid, db)

async def setup(bot):
    info("Economy cog setup called!")
    await bot.add_cog(Economy(bot, cooldown))
