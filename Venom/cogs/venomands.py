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
venom = Venom

class Venomands(commands.Cog):
    def __init__(self, bot: "VenomBot"):
        self.bot = bot

    @commands.command(description="Send a message repeatedly with short intervals", usage="amount, spamtext")
    async def spam(self, ctx: commands.Context, amount: int, *, spamtext: str):
        if ctx.guild is not None:
            perms = ctx.channel.permissions_for(ctx.guild.me)

            convert_bool_to = {False: "❌", True: "✅"}

            def format_permission_row(name, state):
                state_str = convert_bool_to[state]
                return f"  {name:<26} {state_str}"

            header = "  Name                       Value"
            separator = "  ----                       -----"

            formatted_table = f"{header}\n{separator}\n"
            for name, state in perms:
                formatted_table += format_permission_row(name.replace('_', ' ').title(), state) + "\n"
            self.bot.log(venom.INFO, venom.Testing, f"\n{formatted_table}")

        has_slowmode_delay = 0
        if ctx.guild is not None:
            has_slowmode_delay = ctx.channel.slowmode_delay


        if not bool(has_slowmode_delay):
            await self.bot.say(context=ctx, embed=venom.Embed(description=f"✅ spamming {spamtext}", color=venom.Color.green()))
        elif bool(has_slowmode_delay):
            await self.bot.say(context=ctx, embed=venom.Embed(description=f"❌ spamming has no use here\n𝘛𝘩𝘦 𝘤𝘩𝘢𝘯𝘯𝘦𝘭 𝘪𝘴 𝘢𝘳𝘮𝘦𝘥 𝘸𝘪𝘵𝘩 ⏱️𝘴𝘭𝘰𝘸𝘮𝘰𝘥𝘦", color=venom.Color.green()))
            return
        for _ in range(0, int(amount)):
            await ctx.send(spamtext)

    @commands.command()
    async def delete(self, ctx: commands.Context):
        if isinstance(ctx.channel, discord.channel.DMChannel):
            async for m in ctx.channel.history():
                if m.author.id == 530194792701886470:
                    await m.delete(delay=0)

        elif not isinstance(ctx.channel, discord.channel.DMChannel):
            await self.bot.say(context=ctx, embed=venom.Embed(description=":no_entry: Only in DMs, dipshit! bruh", color=venom.Color.red()))


    @commands.command()
    async def messagelogger(self, ctx: commands.Context):
        if self.bot.log_deleted_messages:
            self.bot.log_deleted_messages = False
            await self.bot.say(context=ctx, embed=venom.Embed(description="❌ DISABLED [📨]Message Logger", color=venom.Color.dark_embed()))
        else:
            self.bot.log_deleted_messages = True
            await self.bot.say(context=ctx, embed=venom.Embed(description="✅ ENABLED [📨]Message Logger", color=venom.Color.green()))



    @commands.command()
    async def mimicmessages(self, ctx: commands.Context):
        if self.bot.mimic_messages:
            self.bot.mimic_messages = False
            await self.bot.say(context=ctx, embed=venom.Embed(description="❌ DISABLED [📨]Mimicking Messages", color=venom.Color.dark_embed()))
        else:
            self.bot.mimic_messages = True
            await self.bot.say(context=ctx, embed=venom.Embed(description="✅ ENABLED [📨]Mimicking Messages", color=venom.Color.green()))

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
            await self.bot.say(context=ctx, embed=venom.Embed(description="❌ DISABLED [🛸]Stealth Mode", color=venom.Color.dark_embed()))
        else:
            self.bot.stealth = True
            await self.bot.say(context=ctx, embed=venom.Embed(description="✅ ENABLED [🛸]Stealth Mode", color=venom.Color.green()))

    @commands.command(description="[DEVELOPER] Reload parts of the bot")
    async def reload(self, ctx: commands.Context, cog: str=None):
        if cog is not None:
            resolved_cog = self.bot.get_cog(cog)
            if resolved_cog is None:
                await self.bot.say(context=ctx, embed=venom.Embed(description="🔻 Cog not found", color=venom.Color.red()))
                return
            await self.bot.reload_extension(f"venom.cogs.{resolved_cog.qualified_name.lower()}")
            await self.bot.say(context=ctx, embed=venom.Embed(description=f"✅{resolved_cog.qualified_name} RELOADED", color=venom.Color.green()))

    @commands.command()
    async def clown(self, ctx: commands.Context, messageid: int):
        """"""


async def setup(bot: "VenomBot"):
    await bot.add_cog(Venomands(bot))