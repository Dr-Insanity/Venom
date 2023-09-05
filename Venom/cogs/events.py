from subprocess import run
import discord
from discord.ext import commands
from colorama import init, Fore
from datetime import datetime
from jsontools import get_var, mod_config, del_pair
import platform
from discord.ext.commands import NotOwner,MemberNotFound,RoleNotFound,MessageNotFound,CommandInvokeError,MissingRequiredArgument,MissingPermissions,CommandOnCooldown,CommandNotFound,UserNotFound

init(autoreset=True)

class Events(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command(self, ctx: commands.Context):
        await ctx.message.delete()

    @commands.Cog.listener()
    async def on_command_error(self, i: discord.Interaction, error):
        if isinstance(error, discord.ext.commands.errors.CommandNotFound):
            await i.send(content="**`❌ Die command bestaat niet, kneus `**")
            return
        raise error

async def setup(bot: commands.Bot):
    await bot.add_cog(Events(bot))