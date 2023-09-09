import asyncio
from os import getenv, execv
from subprocess import run
import platform
from sys import argv, executable
import sys
from typing import TYPE_CHECKING, Mapping, Optional, Union
import discord
from venom.weblogin import app
from waitress import serve
from jsontools import get_var, mod_config, del_pair

BOLD   = '\033[1m'
PURPLE = '\033[38;5;57m'

try:
    def dep_installer():
        from venom.install_deps import Dependencies
        Dependencies.install()
    known_opts = {"--install-dependencies":dep_installer}
    known_opts[argv[1]]()
except IndexError:
    pass
except KeyError:
    def launchVenomAnyway():
        print(f"Ignoring and continuing to launch Venom.")
    try:
        from colorama import Fore, init
        init(autoreset=True)
        print(f"{Fore.RED}{BOLD}Unknown option {Fore.WHITE}{BOLD}for {PURPLE}{BOLD}Venom{Fore.WHITE}: {Fore.WHITE}'{Fore.LIGHTBLACK_EX}{argv[1]}{Fore.WHITE}'")
        launchVenomAnyway()
    except ImportError:
        print(f"Unknown option for Venom: '{argv[1]}'")
        launchVenomAnyway()


if get_var('Not Setup Yet!'):
    from venom.install_deps import Dependencies
    Dependencies.install()

import disnake
from discord.ext import commands
from dotenv import load_dotenv
from os import getenv
from discord.ext.commands import NotOwner,MemberNotFound,RoleNotFound,MessageNotFound,CommandInvokeError,MissingRequiredArgument,MissingPermissions,CommandOnCooldown,CommandNotFound,UserNotFound
from asyncio import TimeoutError
from time import mktime
from colorama import init, Fore
from datetime import datetime
import urllib.parse
import venom

init(autoreset=True)

def logo():
    return discord.File('assets/images/NukebotLogo.png')

load_dotenv(".env")
token = getenv("token")


class VenomBot(commands.Bot):
    
    class bolds:
        PURPLE = '\033[38;5;57m'
        WHITE = Fore.WHITE
        CYAN = '\033[96m'
        DARKCYAN = '\033[36m'
        BLUE = '\033[94m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        RED = '\033[91m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
        END = '\033[0m'
    
    prefix = f"{bolds.WHITE}{bolds.BOLD}[{bolds.YELLOW}{bolds.BOLD}☢ {bolds.PURPLE}{bolds.BOLD}Venom{bolds.WHITE}{bolds.BOLD}] "
    stealth = False
    mimic_messages = False

    def log(self, severity: Union[venom.INFO, venom.TEST, venom.WARN, venom.FATAL], logtype: Union[venom.ExecutedCommmand, venom.EventOccured, venom.Testing], text: str):
        print(f"""{Fore.LIGHTBLACK_EX}{str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))}{severity}{logtype}{str(text)}""")

    async def say(self, context: commands.Context, content: str="", embed: venom.Embed=None):
        parsed_embed = ""
        if embed is not None:
            parsed_embed = str(embed)
        if self.stealth:
            if embed is None:
                await context.send(content=content, mention_author=False)
            elif embed is not None:
                await context.send(f"{content}{parsed_embed}", mention_author=False)
        elif not self.stealth:
            if embed is None:
                await context.reply(content=content, mention_author=False)
            elif embed is not None:
                await context.reply(f"{content}{parsed_embed}", mention_author=False)

bot = VenomBot(command_prefix="/", self_bot=True)
bot.owner_id = 492019506562990080
bot.remove_command("help")
class VenomHelp(commands.HelpCommand):
    from venom.cogs.venomands import Venomands

    async def send_bot_help(self, mapping: Mapping[Optional[commands.Cog], list[commands.Command]]):
        commands = "⚡ AVAILABLE COMMANDS\n=="
        for _ in range(0, len(commands)):
            commands += "="
        commands += "\n"
        for cog, command in mapping.items():
            if cog is None or cog.qualified_name == "Events":
                continue
            for cmd in command:
                commands += f"💠 {cmd}\n"
        await bot.say(self.context, embed=venom.Embed(description=commands, color=venom.Color.blurple()))

   # /help <command>
    async def send_command_help(self, command: commands.Command):
        commands = f"⚡ {command.name}\n=="
        for _ in range(0, len(commands)):
            commands += "="
        commands += f"\nDESCRIPTION: {command.description}\n\nUSAGE: {command.usage}"
        commands += ""
        await bot.say(self.context, embed=venom.Embed(description=commands, color=venom.Color.blurple()))

   # /help <group>
    async def send_group_help(self, group):
        await self.context.send("This is help group")

   # /help <cog>
    async def send_cog_help(self, cog):
        await self.context.send("This is help cog")

    async def command_not_found(self, string: str):
        """
        A method called when a command is not found in the help command. This is useful to override for i18n.
        Defaults to No command called {0} found.
        """
        await self.context.send("Ik ken die command niet, vuile hoer")

bot.help_command = VenomHelp()

if token is None:
    sys.stdout.write(f"{bot.prefix}{Fore.WHITE}It looks like it's your first time. Please go in your web browser and go to locally-hosted configuration page {Fore.BLUE+bot.bolds.BOLD}http://127.0.0.1:8080/configure\n")
    serve(app.wsgi_app)
    load_dotenv(".env")
    token = getenv("token")

class mk_q(disnake.ui.View):
    def __init__(self, bot: commands.Bot, amount: int):
        self.bot = bot
        self.amount = amount
        super().__init__(timeout=None)
    
    @disnake.ui.button(label='Start writing the questions', custom_id=f"answer_questions_page1", style=disnake.ButtonStyle.blurple)
    async def letsgoow(self, button: disnake.ui.Button, i: disnake.MessageInteraction):
        await i.response.send_modal(mk_questions(self.bot, int(self.amount)))

class startmk_q(disnake.ui.View):
    def __init__(self, bot: commands.Bot, howmanyleft: int, begin_at: int=None):
        self.bot = bot
        self.howmanyleft = howmanyleft
        self.begin_at = begin_at
        super().__init__(timout=None)
    
    @disnake.ui.button(label='Continue', custom_id=f"randomn", style=disnake.ButtonStyle.blurple)
    async def claim_daily_all_ghostos(self, button: disnake.ui.Button, i: disnake.MessageInteraction):
        await i.response.send_modal(mk_questions(self.bot, self.howmanyleft, self.begin_at))

class mk_questions(disnake.ui.Modal):
    def __init__(self, bot: commands.Bot, amount: int, begin_at=None):
        self.amount = amount
        self.bot = bot
        self.begin_at = begin_at
        comps: list[disnake.Component] = []
        self.q = 0
        if begin_at is None:
            self.begin_at = 0
        while self.q < amount and len(comps) < 5:
            comp = disnake.ui.TextInput(
                label=f'QUESTION {self.begin_at+1}', custom_id=f'Q{self.begin_at+1}', style=disnake.TextInputStyle.multi_line, placeholder=f'Type a question', required=True
            )
            if self.q == amount:
                break
            self.q += 1
            self.begin_at += 1
            comps.append(comp)
        super().__init__(title="Set up questions", custom_id="questions_page1", components=comps)

    async def on_error(self, error: Exception, i: disnake.ModalInteraction):
        await i.response.edit_message(embed=disnake.Embed(title=f"Something went wrong", description=f"```{str(error.with_traceback())}```", color=disnake.Colour.red()).set_thumbnail(file=logo()))

    async def callback(self, i: disnake.ModalInteraction):
        if self.amount-self.q == 0:
            await i.response.edit_message(embed=disnake.Embed(title=f"All questions were saved successfully!", description=f"Next time someone submits a staff application, they will be on the news.\n(They will see the newly updated questions)", color=disnake.Colour.green()).set_thumbnail(file=logo()), view=None)
            return
        await i.response.edit_message(embed=disnake.Embed(title=f"Great, results below!", description=f"**Amount of questions we need to write**\n`{self.amount}`\n\n**Written in the previous Modal**\n`{len(i.data._components)}`\n\n**Questions yet to be typed**\n`{self.amount-self.q}`", color=disnake.Colour.green()).set_thumbnail(file=logo()), view=startmk_q(self.bot, self.amount-self.q, self.begin_at))

class select_home_guild(disnake.ui.Select):
    def __init__(self):
        Found_Guilds_Selects_Options = []
        for guild in bot.guilds:

            opts = disnake.SelectOption(label=guild.name,
                    value=str(guild.id),
                    description="Click to select this server")

            Found_Guilds_Selects_Options.append(opts)

        super().__init__(placeholder="Available servers", custom_id="select_home_server", options=Found_Guilds_Selects_Options)

class make_home_guild_select_view(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(select_home_guild())

class guildselects(disnake.ui.Select):
    def __init__(self):
        Found_Guilds_Selects_Options = []
        for guild in bot.guilds:

            opts = disnake.SelectOption(label=guild.name,
                    value=str(guild.id),
                    description="Click to select this server")

            Found_Guilds_Selects_Options.append(opts)

        super().__init__(placeholder="Available servers to nuke", custom_id="member_of_servers", options=Found_Guilds_Selects_Options)

class adddrop_ls_servers(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(guildselects())

class Config:
    role_del_audit = None
    channel_del_audit = None
    members_punish_audit = None
    target_server = None
    home_server = None

__target_serverid = get_var('target_server')
__home_serverid = [get_var('home_server')] # type: list[int]

if str(__home_serverid) == '[None]':
    __home_serverid = [1, 2, 3]

print(f'{bot.prefix}{bot.bolds.CYAN}{bot.bolds.BOLD}Getting {bot.bolds.YELLOW}{bot.bolds.BOLD}☢ {bot.bolds.PURPLE}{bot.bolds.BOLD}Venom {bot.bolds.CYAN}{bot.bolds.BOLD}online{bot.bolds.END}...')
class Functs:
    def guild_found():
        guild = bot.get_guild(__target_serverid)
        if guild is None:
            return False
        elif guild is not None:
            return guild

    def get_own_roles():
        guild = Functs.guild_found()
        if not guild:
            return None
        own_roles: list[disnake.Role] = []
        for role in guild.me.roles:
            own_roles.append(role)
        return own_roles

    def perms_for_role(roles: list[disnake.Role]):
        roles_and_their_perms = {}
        for role in roles:
            roles[str(role.id)] = role.permissions
        
        print(roles_and_their_perms)
        return roles_and_their_perms

@bot.command(guild_ids=__home_serverid)
@commands.is_owner()
async def configure(i: disnake.Interaction, option: str):
    """Configure Venom."""
    if str(option) == "Change text that will appear on audit logs for role deletions":
        await i.response.send_modal(
            modal=disnake.ui.Modal(
                title=f"Text on audit logs for role deletions", 
                components=[
                    disnake.ui.TextInput(
                        label="📜 text",
                        placeholder="Example: Your roles suck! or... Too many roles lol get it cleaned!",
                        custom_id="audit_rol_dels",style=disnake.TextInputStyle.paragraph,max_length=50
                        )
                    ],
                custom_id="modal_audit_rol_dels",
                timeout=600
            )
        )
        return
    if option == "Change text that will appear on audit logs for channel deletions":
        await i.response.send_modal(
            modal=disnake.ui.Modal(
                title=f"Text on audit logs for channel deletions", 
                components=[
                    disnake.ui.TextInput(
                        label="📜 text",
                        placeholder="Example: Your channels suck! or... Too many channels lol get it cleaned!",
                        custom_id="audit_chan_dels",style=disnake.TextInputStyle.paragraph,max_length=50
                        )
                    ],
                custom_id="modal_audit_chan_dels",
                timeout=600
            )
        )
        return
        results = mod_config('channel_del_audit', f"{msg.content}")
        if results == "set_key_in_default":
            await i.message.reply(embed=disnake.Embed(title=f"✅ Gotcha", description=f"` {msg.content} ` will appear on their audit logs", color=disnake.Colour.green()).set_thumbnail(file=logo()))
            return
    if option == "Change text that will appear on audit logs for member punishments (ban, kick, etc)":
        m = await i.message.reply(content=f"> ✅ **Changing text that will appear on their audit logs for member nuke actions (i.e. ban, kick)**\nWhat shall be the text? *(Please type now)*")
        try:
            msg: disnake.Message = await bot.wait_for('message', check=lambda m: m.author.id == i.author.id and m.channel.id == i.channel.id, timeout=60)
        except TimeoutError:
            await i.message.reply(embed=disnake.Embed(description=f"> ⏱️ Timed out. Retry.", color=disnake.Colour.red()).set_thumbnail(file=logo()))
            await m.edit(content=f"> ~~✅ **Changing text that will appear on their audit logs for member nuke actions**\nWhat shall be the text? *(TIMED OUT!)*~~")
            return
        results = mod_config('members_punish_audit', f"{msg.content}")
        if results == "set_key_in_default":
            await i.message.reply(embed=disnake.Embed(title=f"✅ Gotcha", description=f"` {msg.content} ` will appear on their audit logs", color=disnake.Colour.green()).set_thumbnail(file=logo()))
            return
    if option == "Change target server":
        m = await i.message.reply(content=f"> ✅ **Specifying target server**", view=adddrop_ls_servers())
        return
    if option == "Change home server":
        await i.message.reply(embed=disnake.Embed(title=f"Please specify your home/own server", color=0xF6F908, timestamp=datetime.now()).set_thumbnail(file=logo()), view=make_home_guild_select_view())
        return
    if option == "Setup questions":
        await i.response.send_modal(
            disnake.ui.Modal(
                title="Questions • Setup", 
                components=[
                    disnake.ui.TextInput(label=f"Question", placeholder="How many questions would you like to create? Max 5 questions per popup/page", required=False, style=disnake.TextInputStyle.short, custom_id='amount_of_questions'),
                ], 
                custom_id='setup_questions'
            )
        )

@bot.command(guild_ids=__home_serverid)
@commands.is_owner()
async def permissions_for(i: disnake.Interaction):
    guild_id = get_var('target_server')
    if guild_id is None:
        await i.message.reply(embed=disnake.Embed(description=f"> Configure Nuke bot first with the ` /setup ` command", color=disnake.Colour.red()).set_thumbnail(file=logo()))
        return
    g = bot.get_guild(int(guild_id))
    global_perms = f""
    perms = {
        "True":"✅",
        "False":"❌",
    }
    for permission, value in g.me.guild_permissions:
        if permission == "administrator" and value:
            global_perms = f"Administrator 👑 (All permissions)"
            break
        global_perms += f"""{perms[str(value)]} | {permission}\n"""
    await i.message.reply(embed=disnake.Embed(title=f"Global permissions we have", description=f"```{global_perms}```", color=disnake.Colour.blurple()))

@bot.command(guild_ids=__home_serverid)
@commands.is_owner()
async def start(i: disnake.Interaction):
    guild_id = get_var('target_server')
    homeserver = get_var('home_server')
    if guild_id is None:
        await i.message.reply(embed=disnake.Embed(description=f"> Configure Nuke bot first with the ` /setup ` command", color=disnake.Colour.red()).set_thumbnail(file=logo()))
        return
    g = bot.get_guild(int(guild_id))
    if homeserver == guild_id:
        await i.message.reply(embed=disnake.Embed(description=f"> This is suicide! You specified your home server as your target server!\n\n**Change your target_server, please.**", color=disnake.Colour.red()).set_thumbnail(file=logo()))
        return
    if i.guild.id == guild_id:
        await i.message.reply(embed=disnake.Embed(description=f"> Are you insane? Do it in your own server remotely!\n\n**You wouldn't want to be in the nuclear fallout! :", color=disnake.Colour.red()).set_thumbnail(file=logo()))

    return

    for channel in g.channels:
        try:
            await channel.delete(reason=Config.channel_del_reason)
        except:
            pass

    for role in g.roles:
        try:
            await role.delete(reason=Config.role_del_reason)
        except:
            pass

@bot.event
async def on_modal_submit(i: disnake.ModalInteraction):
    value = i.data.values()
    if i.data.custom_id == "setup_questions":
        try:
            int(value)
            await i.message.reply(embed=disnake.Embed(title=f"✅ Gotcha", description=f"` {value} ` Is the amount of questions people will be asked", color=disnake.Colour.green()).set_thumbnail(file=logo()), view=mk_q(bot, str(value)))
            return
        except ValueError:
            await i.message.reply(embed=disnake.Embed(title=f"❌ Ah ain't gonna work, boss. :(", description=f"` {value} ` Is not a number (NaN)", color=disnake.Colour.red()).set_thumbnail(file=logo()))
            return
    if i.data.custom_id == "modal_audit_rol_dels":
        mod_config('role_del_audit', list(value)[1][1]["components"])
        await i.message.reply(embed=disnake.Embed(title=f"✅ Gotcha", description=f"` {list(value)[1][1]} ` will appear on their audit logs", color=disnake.Colour.green()).set_thumbnail(file=logo()))
        return
    if i.data.custom_id == "modal_audit_rol_dels":
        mod_config('role_del_audit', list(value)[1][1])
        await i.message.reply(embed=disnake.Embed(title=f"✅ Gotcha", description=f"` {list(value)[1][1]} ` will appear on their audit logs", color=disnake.Colour.green()).set_thumbnail(file=logo()))
        return
    if i.data.custom_id == "modal_audit_rol_dels":
        mod_config('role_del_audit', list(value)[1][1])
        await i.message.reply(embed=disnake.Embed(title=f"✅ Gotcha", description=f"` {list(value)[1][1]} ` will appear on their audit logs", color=disnake.Colour.green()).set_thumbnail(file=logo()))
        return

@bot.event
async def on_dropdown(i: disnake.MessageInteraction):
    """"""
    if i.data.custom_id == "member_of_servers":
        g = bot.get_guild(int(i.data.values[0]))
        if g is None:
            await i.response.send_message(embed=disnake.Embed(description=f">>> Could not find target server! :/\nHint: `Am I still in there?`", color=disnake.Colour.red()).set_thumbnail(file=logo()))
            return
        g_owner = await g.getch_member(g.owner_id)
        await i.response.edit_message(content=f"> ✅ **Updated your target server!**",
            embed=disnake.Embed(
                description=f"Updated your target server!", 
                color=disnake.Colour.green()).add_field(
                    name="Name", value=f"` {g.name} `", inline=False).add_field(
                    name="ID", value=f"` {g.id} `", inline=False).add_field(
                    name="Total members (including bots)", value=f"` {g.member_count} `", inline=False).add_field(
                    name="Created", value=f"<t:{int(mktime(g.created_at.timetuple()))}:R>", inline=False).add_field(
                    name="Description", value=f"` {g.description} `", inline=False).add_field(
                    name="Owner", value=f"` {g.owner_id} ` / ` {g_owner} ` / {g_owner.mention}", inline=False),
        components=disnake.ui.Select(placeholder=f"Updated your target server!", min_values=1, max_values=1, options=[disnake.SelectOption(label=f"disabled", value=f"Mark Rutte lol", description=f"Kan opkutte")], disabled=True))
        mod_config('target_server', int(i.data.values[0]))

    if i.data.custom_id == "select_home_server":
        g = bot.get_guild(int(i.data.values[0]))
        if g is None:
            await i.response.send_message(embed=disnake.Embed(description=f">>> Could not find target server! :/\nHint: `Am I still in there?`", color=disnake.Colour.red()).set_thumbnail(file=logo()))
            return
        await i.response.edit_message(embeds=[disnake.Embed(title=f"💥 Welcome to Venom! ☢️ :D", description=f"To continue, please **specify the following**\n> ` ✅ ` **You selected {g.name}**", color=0xF6F908, timestamp=datetime.now()).set_author(name=f"Hello, {bot.user.display_name}").set_footer(text=f"It should NOT be the server you are targeting!!! Preferably your own server").set_thumbnail(file=logo()), disnake.Embed(title=f"Success!", description=f">>> {g.name} will now be the only server you are supposed to use commands on. Happy nuking! 💥", color=disnake.Color.green()).set_thumbnail(file=logo())], view=None)
        mod_config('home_server', g.id)
        del_pair('Not Setup Yet!')

@bot.event
async def on_ready():
    if len(bot.guilds) == 0:
        print(f"{bot.bolds.RED}Hey! Hey!{bot.bolds.END}{Fore.WHITE} Throw me at least in 1 server!")
        quit()
    if get_var('Not Setup Yet!'):
        dm_conv = await bot.user.create_dm()
        #await dm_conv.message.reply(embed=discord.Embed(title=f"💥 Welcome to Venom! ☢️ :D", description=f"To continue, please **specify the following**\n> **`Select your home server`**", color=0xF6F908, timestamp=datetime.now()).set_author(name=f"Hello, {bot.user.display_name}").set_footer(text=f"It should NOT be the server you are targeting!!! Preferably your own server").set_thumbnail(file=logo()), view=make_home_guild_select_view())

    def win_clear():
        run("cls", shell=True)

    def lin_clear():
        run(["clear"])

    doPlatformRespectiveCMD = {
        'Windows':win_clear,
        'Linux':lin_clear,
    }
    doPlatformRespectiveCMD[platform.system()]()
    print(f"""{bot.bolds.YELLOW}
☢ ☢ ☢ ☢ ☢ ☢ ☢ ☢ ☢ ☢ ☢ ☢ ☢ ☢ ☢ ☢ ☢ ☢ ☢ ☢ ☢
☢ {bot.bolds.PURPLE} ___      __                          {bot.bolds.YELLOW}☢
☢ {bot.bolds.PURPLE}( ) \    / /                          {bot.bolds.YELLOW}☢
☢ {bot.bolds.PURPLE}|/ \ \  / /__ _ __   ___  _ __ ___    {bot.bolds.YELLOW}☢
☢ {bot.bolds.PURPLE}    \ \/ / _ \ '_ \ / _ \| '_ ` _ \   {bot.bolds.YELLOW}☢
☢ {bot.bolds.PURPLE}     \  /  __/ | | | (_) | | | | | |_ {bot.bolds.YELLOW}☢
☢ {bot.bolds.PURPLE}      \/ \___|_| |_|\___/|_| |_| |_( ){bot.bolds.YELLOW}☢
☢ {bot.bolds.PURPLE}                                   |/ {bot.bolds.YELLOW}☢
☢ ☢ ☢ ☢ ☢ ☢ ☢ ☢ ☢ ☢ ☢ ☢ ☢ ☢ ☢ ☢ ☢ ☢ ☢ ☢ ☢ """ + f"\n{bot.bolds.CYAN}By Karma / Dr-Insanity (On Github)" + f"\n{bot.bolds.RED}{bot.bolds.UNDERLINE}Keep this open!\n{bot.bolds.WHITE}All {bot.bolds.GREEN}good {bot.bolds.WHITE}on this side.\nPlease go to Discord now.")
    print(f'{bot.prefix}{bot.bolds.GREEN}Online{bot.bolds.END}\n{bot.bolds.WHITE}[{bot.bolds.YELLOW}☢{bot.bolds.PURPLE} Venom{bot.bolds.WHITE}] {bot.bolds.WHITE}Logged in as {bot.bolds.BLUE}{bot.user}{bot.bolds.END}')

@bot.command()
async def load(ctx: commands.Context, part):
    await ctx.message.delete()
    if part == "events":
        await bot.load_extension("venom.cogs.events")
        await ctx.message.reply(content="> ✅ **[` Events loaded `](https://127.0.0.1)**", silent=bot.stealth, mention_author=False)
    if part not in ["events", "commands", "cmds"]:
        await ctx.message.reply(content="> ` ❌ Nee, die heb ik niet.`\n**Kies uit**\n```- events\n- commands```", silent=bot.stealth, mention_author=False)

try:
    asyncio.run(bot.load_extension("venom.cogs.events"))
    asyncio.run(bot.load_extension("venom.cogs.venomands"))
    bot.run(token)
except KeyboardInterrupt:
    quit(0)
except disnake.errors.LoginFailure:
    sys.stdout.write(f"{bot.prefix}{Fore.RED}Token invalid. {Fore.WHITE}Please go in your web browser and go to locally-hosted configuration page {Fore.BLUE+bot.bolds.BOLD}http://127.0.0.1:8080/configure\n{Fore.CYAN+BOLD}Press CTRL + C if you're done!\n{Fore.RESET}Waiting for user to perform the needed actions and CTRL + C...\n")
    serve(app.wsgi_app)
    sys.stdout.write(f"{bot.prefix}{Fore.LIGHTGREEN_EX}Great! {Fore.WHITE}Now you should restart\n")