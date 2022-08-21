import json
from sys import argv

def mod_config(key: str, value):
    with open("conf.json", "r") as jsonfile:
        data = json.load(jsonfile)
        jsonfile.close()
        
    data[key] = value
    with open("conf.json", "w+") as jsonfile:
        myJSON = json.dump(data, jsonfile, indent=2)
        jsonfile.close()

def del_pair(key: str):
    with open("conf.json", "r") as jsonfile:
        data = json.load(jsonfile)
        jsonfile.close()

    del data[key]
    with open("conf.json", "w+") as jsonfile:
        myJSON = json.dump(data, jsonfile, indent=2)
        jsonfile.close()

if argv[1] == "--delete-pair" or argv[1] == "-d":
    del_pair(argv[2])
elif argv[1] == "--add-pair" or argv[1] == "-a":
    mod_config(argv[2], argv[3])
else:
    print(f"invalid option: '{argv[1]}'")