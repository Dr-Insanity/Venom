from subprocess import run
import discord
from discord.ext import commands
from colorama import init, Fore
from datetime import datetime
from jsontools import get_var, mod_config, del_pair
import platform
from discord.ext.commands import NotOwner,MemberNotFound,RoleNotFound,MessageNotFound,CommandInvokeError,MissingRequiredArgument,MissingPermissions,CommandOnCooldown,CommandNotFound,UserNotFound
from typing import TYPE_CHECKING
import venom
if TYPE_CHECKING:
    from main import VenomBot

init(autoreset=True)

class Venomands(commands.Cog):
    def __init__(self, bot: "VenomBot"):
        self.bot = bot

    @commands.command()
    async def spam(self, ctx: commands.Context, amount: int, *, spamtext: str):
        convert_bool_to = {False: "❌", True: "✅"}
        for permission, state in ctx.channel.permissions_for(ctx.guild.me):
            print(f"""{permission} --> {convert_bool_to[state]}""")
        
        await self.bot.say(context=ctx, embed=venom.Embed(description=f"Spam aborted, command in testing mode", color=venom.Color.green()))
        #await self.bot.say(context=ctx, embed=venom.Embed(description=f"✅ Spamming {spamtext}", color=venom.Color.green()))
        #for a in range(0, int(amount)):
        #    await ctx.send(spamtext)

    @commands.command()
    async def delete(self, ctx: commands.Context):
        user = self.bot.get_user(self.bot.owner_id) # type: discord.User
        await ctx.message.delete()
        if isinstance(ctx.channel, discord.channel.DMChannel):
            async for message in ctx.channel.history():
                if message.author.id == 530194792701886470:
                    await message.delete(delay=0)

        elif not isinstance(ctx.channel, discord.channel.DMChannel):
            await self.bot.say(context=ctx, embed=venom.Embed(description=":no_entry: Only in DMs, dipshit! bruh", color=venom.Color.red()))

    @commands.command()
    async def mimic_messages(self, ctx: commands.Context):
        if self.bot.mimic_messages:
            self.bot.mimic_messages = False
            await self.bot.say(context=ctx, embed=venom.Embed(description="❌ DISABLED [📨]Mimicking Messages"))
        else:
            self.bot.mimic_messages = True
            await self.bot.say(context=ctx, embed=venom.Embed(description="✅ ENABLED [https://gist.github.com/whitingx/3840905]Mimicking Messages", color=venom.Color.green()))

    @commands.command()
    async def idle(self, ctx: commands.Context):
        status = str(self.bot.status)
        if status != "idle":
            await self.bot.change_presence(status=discord.Status.idle)
            await self.bot.say(context=ctx, embed=venom.Embed(description=f"""✅ Your status is changed from "{status}" to "idle" """, color=venom.Color.green()))
            return
        await self.bot.say(context=ctx, embed=venom.Embed(description=f"""🔻 Your status is already on "idle", dumbass""", color=venom.Color.red()))

    @commands.command()
    async def dnd(self, ctx: commands.Context):
        status = str(self.bot.status)
        if status != "dnd":
            await self.bot.change_presence(status=discord.Status.dnd)
            await self.bot.say(context=ctx, embed=venom.Embed(description=f"""✅ Your status is changed from "{status}" to "dnd" """, color=venom.Color.green()))
            return
        await self.bot.say(context=ctx, embed=venom.Embed(description=f"""🔻 Your status is already on "dnd", dumbass""", color=venom.Color.red()))

    @commands.command()
    async def on(self, ctx: commands.Context):
        status = str(self.bot.status)
        if status != "online":
            await self.bot.change_presence(status=discord.Status.online)
            await self.bot.say(context=ctx, embed=venom.Embed(description=f"""✅ Your status is changed from "{status}" to "online" """, color=venom.Color.green()))
            return
        await self.bot.say(context=ctx, embed=venom.Embed(description=f"""🔻 Your status is already on "online", dumbass""", color=venom.Color.red()))

    @commands.command()
    async def stealthmode(self, ctx: commands.Context):
        if self.bot.stealth:
            self.bot.stealth = False
            await ctx.send(embed=venom.Embed(description="❌ DISABLED [🛸]Stealth Mode", color=venom.Color.dark_embed()))
        else:
            self.bot.stealth = True
            await self.bot.say(context=ctx, embed=venom.Embed(description="✅ ENABLED [🛸]Stealth Mode", color=venom.Color.green()))

    @commands.command()
    async def reload(self, ctx: commands.Context, cog: str=None):
        if cog is not None:
            resolved_cog = self.bot.get_cog(cog)
            if resolved_cog is None:
                await self.bot.say(context=ctx, embed=venom.Embed(description="🔻 Cog niet gevonden, kneus", color=venom.Color.red()))
                return
            await self.bot.reload_extension(f"Venom.cogs.{resolved_cog.qualified_name.lower()}")
            await self.bot.say(context=ctx, embed=venom.Embed(description=f"✅{resolved_cog.qualified_name} RELOADED", color=venom.Color.green()))

    @commands.command()
    async def clown(self, ctx: commands.Context, messageid: int):
        """"""


async def setup(bot: "VenomBot"):
    await bot.add_cog(Venomands(bot))