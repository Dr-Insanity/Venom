from subprocess import run
import discord
from discord.ext import commands
from colorama import init, Fore
from datetime import datetime
from jsontools import get_var, mod_config, del_pair
import platform
from discord.ext.commands import NotOwner,MemberNotFound,RoleNotFound,MessageNotFound,CommandInvokeError,MissingRequiredArgument,MissingPermissions,CommandOnCooldown,CommandNotFound,UserNotFound
from typing import TYPE_CHECKING
import Venom
if TYPE_CHECKING:
    from main import VenomBot

init(autoreset=True)

class Events(commands.Cog):
    def __init__(self, bot: "VenomBot"):
        self.bot = bot
        self.DMd_people = [] # type: list[int]
        self.server_mimicked_people = [] # type: list[int]

    @commands.Cog.listener()
    async def on_command(self, ctx: commands.Context):
        if self.bot.stealth:
            await ctx.message.delete()

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        if self.bot.stealth:
            await ctx.message.delete()
        if isinstance(error, discord.ext.commands.errors.CommandNotFound):
            await self.bot.say(context=ctx, embed=Venom.Embed(description="🔻 Die command bestaat niet, kneus", color=Venom.Color.red()))
            return
        if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await self.bot.say(context=ctx, embed=Venom.Embed(description="🔻 Ik mis een argument, botje! 🦴💀", color=Venom.Color.red()))
            return
        raise error
    
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.id == self.bot.user.id:
            return
        if isinstance(message.channel, discord.channel.DMChannel):
            if self.bot.mimic_messages:
                if message.author.id not in self.DMd_people:
                    await message.reply(content=f"**🤡:** {message.content}")
                    self.DMd_people.append(message.author.id)
        else:
            if self.bot.mimic_messages:
                if message.author.id not in self.server_mimicked_people:
                    await message.reply(content=f"**🤡:** {message.content}")
                    self.server_mimicked_people.append(message.author.id)

async def setup(bot: "VenomBot"):
    await bot.add_cog(Events(bot))