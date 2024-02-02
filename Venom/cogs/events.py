from subprocess import run
import discord
from discord.ext import commands
from colorama import init, Fore
from datetime import datetime, timedelta
from jsontools import get_var, mod_config, del_pair
import platform
from discord.ext.commands import NotOwner,MemberNotFound,RoleNotFound,MessageNotFound,CommandInvokeError,MissingRequiredArgument,MissingPermissions,CommandOnCooldown,CommandNotFound,UserNotFound
import Venom
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main import VenomBot

venom = Venom

INFO  = venom.INFO
TEST  = venom.TEST
WARN  = venom.WARN
FATAL = venom.FATAL

ExecutedCommand = venom.ExecutedCommmand
EventOccured = venom.EventOccured
DeletedMessage = venom.OccuredEventTypes.DeletedMessage
CommanD = venom.OccuredEventTypes.Command
BulkDeletedMessage = venom.OccuredEventTypes.BulkDeletedMessages

init(autoreset=True)

class Events(commands.Cog):
    def __init__(self, bot: "VenomBot"):
        self.bot = bot
        self.DMd_people = [] # type: list[int]
        self.server_mimicked_people = [] # type: list[int]
        self.deleted_messages = [] # type: list[int]

    @commands.Cog.listener()
    async def on_command(self, ctx: commands.Context):
        if self.bot.stealth:
            await ctx.message.delete()
        self.bot.log(INFO(), EventOccured(CommanD(self.bot.stealth)), f"The '{ctx.prefix}{ctx.command}' is ran with success")

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        if self.bot.stealth:
            await ctx.message.delete()
        if isinstance(error, discord.ext.commands.errors.CommandNotFound):
            await self.bot.say(context=ctx, embed=venom.Embed(description=f"🔻 '{error}' does not exist", color=venom.Color.red()))
            return
        if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await self.bot.say(context=ctx, embed=venom.Embed(description=f"🔻 Missing arguments.", color=venom.Color.red()))
            await ctx.send_help(ctx.command)
            return
        raise error

    @commands.Cog.listener()
    async def on_message_delete(self, m: discord.Message):
        #if m.author.id == self.bot.user.id:
        #    return
        if isinstance(m.channel, discord.channel.DMChannel):
            if self.bot.log_deleted_messages:
                self.bot.log(INFO(), EventOccured(DeletedMessage()), f"""{m.author} DELETED:\n\n{Fore.GREEN}"{Fore.CYAN}{m.content}{Fore.GREEN}" """)
        if not m.author.bot:
            self.bot.deleted_messages.append(m.author.id)
            if self.bot.deleted_messages.count(m.author.id) == 15: # 10 MESSAGES MUST BE IN THERE. EVERY 10 SECONDS, THE LIST IS CLEANED
                self.bot.log(WARN(), EventOccured(DeletedMessage()), f"Other selfbot detected! It's {Fore.RED+self.bot.bolds.BOLD}{m.author} {Fore.GREEN+self.bot.bolds.BOLD}{m.author.id}")
                for userid in self.bot.deleted_messages:
                    if userid == m.author.id:
                        self.bot.deleted_messages.remove(userid)

    @commands.Cog.listener()
    async def on_message(self, m: discord.Message):
        if m.author.id == self.bot.user.id:
            return
        if isinstance(m.channel, discord.channel.DMChannel):
            if self.bot.mimic_messages:
                if m.author.id not in self.DMd_people:
                    await m.reply(content=f"**🤡:** {m.content}")
                    self.DMd_people.append(m.author.id)
        else:
            if m.guild.id not in [267624335836053506]:
                if self.bot.mimic_messages:
                    if m.author.id not in self.server_mimicked_people:
                        await m.reply(content=f"**🤡:** {m.content}")
                        self.server_mimicked_people.append(m.author.id)
                if not m.author.bot:
                    user = m.author
                    joined = m.author.joined_at # type: datetime
                    now = m.created_at
                    time_in_between = now - joined

                    if time_in_between.days == 0 and time_in_between.seconds > 0 and time_in_between.seconds < 300:
                        if "http://" in m.content or "https://" in m.content:
                            await m.channel.send(
                                content=f"# :warning: warning\nYou are flagged for potentially being a selfbot.\nYou are **advised** to stop posting links."
                            )
                            # considered selfbot? No. User can be fresh and just posted a link
                            # keep them monitored

                            accessible_channels = []
                            for channel in m.guild.channels:
                                for p, s in channel.permissions_for(m.author):
                                    if p == 'send_messages' and str(s) == 'True':
                                        accessible_channels.append(accessible_channels)

                            self.bot.flagged_accounts[user.id] = {
                                "message_count":"",
                                "pattern":m.content,
                                "":"",
                            }

def setup(bot: "VenomBot"):
    bot.add_cog(Events(bot))