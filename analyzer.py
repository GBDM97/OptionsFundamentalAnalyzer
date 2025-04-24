from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from filesUtils import exportOutput, importFile, importYahooAssetData
from pyjs import fetch_br_fundamentals, fetch_us_fundamentals

etfsArray = [
    "BOVA11.SA"
]

def create_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("window-size=200,500")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36")
    service = Service(executable_path='C:\\Users\\cvp14567\\Downloads\\chromedriver.exe')
    return webdriver.Chrome(service=service, options=options)

def start():
    def areDebtValuesValid(d):
        if( 
            (not d[0] or d[0] > 0) and
            (not d[1] or d[1] < 1) and
            (not d[2] or d[2] < 2) and
            (not d[3] or d[3] < 2) and
            (not d[5] or d[5] < 1) and
            (not d[6] or d[6] > 1)
        ):
            if(not d[0] and not d[1] and not d[2] and not d[3] and not d[4] and not d[5] and not d[6]):
                return False
            return True
        return False
    
    def areDebtValuesInvalid(d):
        if( 
            (not d[0] or d[0] < 0) and
            (not d[2] or d[2] > 2) and
            (not d[3] or d[3] > 2) and
            (not d[6] or d[6] < 1)
        ):
            if(not d[0] and not d[1] and not d[2] and not d[3] and not d[4] and not d[5] and not d[6]):
                return False
            return True
        return False
    
    def getLastAnalyzedIndex(l, lastAsset):
        if lastAsset:
            for i,v in enumerate(l):
                if v[0] == lastAsset:
                    return i
        return 0

    driver = create_driver()
    driver.get("https://statusinvest.com.br")
    selectedAssets = []
    assets = importYahooAssetData()
    outputFile = importFile('output')
    if outputFile:
        lastRegisteredAsset = outputFile[-1][0]
        selectedAssets = outputFile
        lastIndex = getLastAnalyzedIndex(assets, lastRegisteredAsset)+1
    else: 
        lastRegisteredAsset = ''
        lastIndex = getLastAnalyzedIndex(assets, lastRegisteredAsset)
    print(len(assets))

    for index,asset in enumerate(assets[lastIndex:], start=lastIndex):
        errors = []
        print(str(index+1)+f" Fetching data for: {asset[0]}")
        if asset[0] in etfsArray:
            fundamentalsData = {
                "debts":[1,0,0,0,1,0,2],
                "results":[1]
            }
        elif asset[0][-3:] == '.SA':
            fundamentalsData = fetch_br_fundamentals(driver, asset[0])
        else:
            fundamentalsData = fetch_us_fundamentals(driver, asset[0])
            
        try:
            debtValid = areDebtValuesValid(fundamentalsData['debts'])
            debtInvalid = areDebtValuesInvalid(fundamentalsData['debts'])

            if (fundamentalsData['results']):
                if (all(n > 0 for n in fundamentalsData['results']) and debtValid):
                    asset.append('Good fundamentals')
                    selectedAssets.append(asset)
                if (any(n < 0 for n in fundamentalsData['results']) and debtInvalid):
                    asset.append('Bad fundamentals')
                    selectedAssets.append(asset)
            if str(index)[-2:] == '00':
                exportOutput(selectedAssets)
        except Exception as error:
            errors.append(error)
            continue
    
    exportOutput(selectedAssets)
    print('Data exported!')
    driver.quit()

if __name__ == '__main__':
    start()