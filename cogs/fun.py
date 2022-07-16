from discord.ext import commands
import discord, logging, random
from discord import app_commands
import mtg2, os

logger = logging.getLogger("Fun")

info = logger.info


class Fun(commands.Cog):
    def __init__(self, bot):
        info("Loading fun cog...")
        self.bot = bot
        info("Done!")
        # This context menu command only works on messages
        @bot.tree.context_menu(name='Report to Moderators')
        async def report_message(interaction: discord.Interaction, message: discord.Message):
            # We're sending this response message with ephemeral=True, so only the command executor can see it
            await interaction.response.send_message(
                f'Thanks for reporting this message by {message.author.mention} to our moderators.', ephemeral=True
            )

            # Handle report by sending it into a log channel
            log_channel = interaction.guild.get_channel(984536404178653264)  # replace with your channel id

            embed = discord.Embed(title='Reported Message')
            if message.content:
                embed.description = message.content

            embed.set_author(name=message.author.display_name, icon_url=message.author.display_avatar.url)
            embed.timestamp = message.created_at

            url_view = discord.ui.View()
            url_view.add_item(discord.ui.Button(label='Go to Message', style=discord.ButtonStyle.url, url=message.jump_url))

            await log_channel.send(embed=embed, view=url_view)
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

    @commands.command(aliases=["табличка"])
    async def gentable(self, ctx, text="text", color=None):
        if color != None:
            color = mtg2.ColourRGBA(color)
            mtg2.generate_table(text, color).save("/tmp/table.png")
        else: mtg2.generate_table(text).save("/tmp/table.png")
        await ctx.send(file=discord.File("/tmp/table.png"))
        os.remove("/tmp/table.png")


async def setup(bot):
    await bot.add_cog(Fun(bot))