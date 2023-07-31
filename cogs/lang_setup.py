from discord.ext import commands
import discord
from modules.bundles import Bundle

class LangSetup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bundle = Bundle()
    @commands.Cog.listener("on_guild_join")
    async def bruh(self, guild: discord.Guild):
        await guild.channels[0].send("Thanks for adding me, you can set my language using command |lang lang\nExample: To set english: |lang en_US\nTo set russian: |lang ru_RU\nMy default language is english.")
        self.bundle.setlang(guild.id, "en_US")
    @commands.command(help="Sets language for server, if language is valid, bot sends nothing.")
    @commands.has_permissions(manage_roles=True, ban_members=True, administrator=True)
    async def lang(self, ctx: commands.Context, lang, *argv):
        if self.bundle.getbundlelang(lang) == {}:
            await ctx.send(self.bundle.get(ctx.guild.id, "lang.notvalid").format(lang=lang))
        else:
            self.bundle.setlang(ctx.guild.id, lang)

async def setup(bot: commands.Bot):
    await bot.add_cog(LangSetup(bot))