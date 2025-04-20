import json

def importIVList():
    with open("iv.json", "r") as file:
        return json.loads(file.read())