from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from filesUtils import exportOutput, importFile, importYahooAssetData

def create_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36")
    service = Service(executable_path='C:\\Users\\cvp14567\\Downloads\\chromedriver.exe')
    return webdriver.Chrome(service=service, options=options)

def fetch_fundamentals(driver, ticker):
    js_code = f"""
    const callback = arguments[arguments.length - 1]; // Needed for execute_async_script

    (async () => {{
        const output = {{
            results: [],
            debts: []
        }};

        try {{
            const htmlResponse = await fetch("https://statusinvest.com.br/acoes/eua/{ticker}");
            const html = await htmlResponse.text();
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');

            const xpaths = [
                '/html/body/main/div[3]/div/div/div[2]/div/div[2]/div/div[1]/div/div/strong',
                '/html/body/main/div[3]/div/div/div[2]/div/div[2]/div/div[2]/div/div/strong',
                '/html/body/main/div[3]/div/div/div[2]/div/div[2]/div/div[3]/div/div/strong',
                '/html/body/main/div[3]/div/div/div[2]/div/div[2]/div/div[4]/div/div/strong',
                '/html/body/main/div[3]/div/div/div[2]/div/div[2]/div/div[5]/div/div/strong',
                '/html/body/main/div[3]/div/div/div[2]/div/div[2]/div/div[6]/div/div/strong'
            ];

            output.debts = xpaths.map(xpath => {{
                const node = doc.evaluate(xpath, doc, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                return node ? parseFloat(node.textContent.trim().replaceAll('.','').replaceAll(',','.')) : null;
            }});

            const companyId = doc.querySelector('div[data-companyid]')?.getAttribute('data-companyid');

            if (companyId) {{
                const jsonRes0 = await fetch(`https://statusinvest.com.br/stock/getincomestatment?companyid=${{companyId}}&type=0&futureData=false`);
                const jsonRes1 = await fetch(`https://statusinvest.com.br/stock/getincomestatment?companyid=${{companyId}}&type=1&futureData=false`);
                const json0 = await jsonRes0.json();
                const json1 = await jsonRes1.json();

                output.debts.unshift(
                    parseFloat(json0.data.grid[10].columns[1].value.replaceAll(',','.').replaceAll(' M',''))
                );

                output.results = json1.data.grid[18].gridLineModel.values;
            }}

            callback(output); // THIS sends data back to Python

        }} catch (err) {{
            callback({{ error: err.message || 'Unknown error' }}); // Ensure error is returned too
        }}
    }})();
    """
    return driver.execute_async_script(js_code)

def start():
    def areDebtValuesValid(d):
        if( 
            (not d[0] or d[0] > 0) and
            (not d[1] or d[1] < 1) and
            (not d[2] or d[2] < 2) and
            (not d[3] or d[3] < 2) and
            (not d[4] or d[4] > 0.4) and
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
        for i,v in enumerate(l):
            if v[0] == lastAsset:
                return i
        return 0

    driver = create_driver()
    driver.get("https://statusinvest.com.br")
    selectedAssets = []
    assets = importYahooAssetData()
    outputFile = importFile('output')
    lastRegisteredAsset = outputFile[-1][0] if outputFile else ''
    lastIndex = getLastAnalyzedIndex(assets, lastRegisteredAsset)
    print(len(assets))

    for index,asset in enumerate(assets[lastIndex:], start=lastIndex):
        errors = []
        print(str(index+1)+f" Fetching data for: {asset[0]}")
        fundamentalsData = fetch_fundamentals(driver, asset[0])
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