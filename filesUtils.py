import json

def importIVList():
    with open("data\\barchartIV.json", "r") as file:
        return json.loads(file.read())
    
def importTradingviewAssets():
    with open("data\\tradingviewAssets.json", "r") as file:
        return json.loads(file.read())

def importYahooAssetData():
    with open("data\\yahooAssetData.json", "r") as file:
        return json.loads(file.read())
    
def exportOutput(l):
    with open("data\\output.json", "w") as file:
        json.dump(l, file, indent=1)

def exportErrors(l):
    with open("data\\errors.json", "w") as file:
        json.dump(l, file, indent=1)

def exportYahooAssetData(l):
    with open("data\\yahooAssetData.json", "w") as file:
        json.dump(l, file, indent=1)