from subprocess import run
import discord
from discord.ext import commands
from colorama import init, Fore
from datetime import datetime
from jsontools import get_var, mod_config, del_pair
import platform
from discord.ext.commands import NotOwner,MemberNotFound,RoleNotFound,MessageNotFound,CommandInvokeError,MissingRequiredArgument,MissingPermissions,CommandOnCooldown,CommandNotFound,UserNotFound
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main import VenomBot

init(autoreset=True)

class Venomands(commands.Cog):
    def __init__(self, bot: "VenomBot"):
        self.bot = bot

    @commands.command()
    async def mimic_messages(self, ctx: commands.Context):
        if self.bot.mimic_messages:
            self.bot.mimic_messages = False
            await ctx.message.reply(content="> ❌**` DISABLED [📨]Mimicking Messages `**", silent=self.bot.stealth, mention_author=False)
        else:
            self.bot.mimic_messages = True
            await ctx.message.reply(content="> ✅**` ENABLED [📨]Mimicking Messages `**", silent=self.bot.stealth, mention_author=False)

    @commands.command()
    async def mimic_messages(self, ctx: commands.Context):
        if self.bot.stealth:
            self.bot.stealth = False
            await ctx.message.reply(content="> ❌**` DISABLED [📨]Stealth Mode `**", silent=self.bot.stealth, mention_author=False)
        else:
            self.bot.stealth = True
            await ctx.message.reply(content="> ✅**` ENABLED [📨]Stealth Mode `**", silent=self.bot.stealth, mention_author=False)

    @commands.command()
    async def reload(self, ctx: commands.Context, cog: str=None):
        if cog is not None:
            resolved_cog = self.bot.get_cog(cog)
            if resolved_cog is None:
                await ctx.message.reply(content="> ⛔**` Cog niet gevonden, kneus `**", silent=self.bot.stealth)
                return
            await resolved_cog.cog_unload()
            await ctx.message.reply(content="> ✅**` Cog Unloaded `**", silent=self.bot.stealth, mention_author=False)
            await resolved_cog.cog_load()
            await ctx.message.reply(content="> ✅**` Cog RELOADED `**", silent=self.bot.stealth, mention_author=False)

    

async def setup(bot: "VenomBot"):
    await bot.add_cog(Venomands(bot))