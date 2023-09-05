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
        except Exception as e:
            print(e)