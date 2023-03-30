from colorama import Fore, init
import disnake
from flask import Flask, render_template, request
from configparser import ConfigParser, NoOptionError

conf = ConfigParser()
init(autoreset=True)
app = Flask('client', static_folder="Venom/static", template_folder="Venom/templates")

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

@app.before_request
def before_serving():
    conf.read('./config/config.ini')
    try:
        tok = conf.get(section='DEFAULT', option='token')
    except NoOptionError:
        return

@app.route('/configure')
def config():
    return render_template("index.html")

@app.route('/configure/completed', methods=['POST'])
def haum():
    if request.method == 'POST':
        form = request.form
        
        #f = open(".env", "w+")
        #f.write(f"token={str(form.get('bot_token'))}")
        #f.close()
        print(f"{bolds.WHITE}{bolds.BOLD}[{bolds.YELLOW}{bolds.BOLD}☢ {bolds.PURPLE}{bolds.BOLD}Venom{bolds.WHITE}{bolds.BOLD}] {bolds.PURPLE}{bolds.BOLD}Venom {bolds.WHITE}is now {Fore.LIGHTGREEN_EX}restarting!")
        return render_template("success.html")