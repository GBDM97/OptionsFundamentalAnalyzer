import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# List of assets (tickers) to process
# const allFundamentals = []

def importIVList():
    with open("iv.json", "r") as file:
        return json.loads(file.read())

def create_driver():
    options = Options()
    # options.add_argument("--headless")  # headless mode
    # options.add_argument("--disable-gpu")
    # options.add_argument("--no-sandbox")
    # options.add_argument("--disable-dev-shm-usage")
    options.add_argument("window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36")
    service = Service(executable_path='C:\\Users\\cvp14567\\Downloads\\chromedriver.exe')  # Change path accordingly
    return webdriver.Chrome(service=service, options=options)

def fetch_data_for_asset(driver, ticker):
    js_code = f"""
    return (async () => {{
        const output = {{
            resultValues: [],
            debtValues: []
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

            output.debtValues = xpaths.map(xpath => {{
                const node = doc.evaluate(xpath, doc, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                return node ? node.textContent.trim() : null;
            }});

            const companyId = doc.querySelector('div[data-companyid]')?.getAttribute('data-companyid');

            if (companyId) {{
                const jsonRes = await fetch(`https://statusinvest.com.br/stock/getincomestatment?companyid=${{companyId}}&type=1&futureData=false`);
                const json = await jsonRes.json();
                output.resultValues = json.data.grid[18].gridLineModel.values;
            }}

            return output;

        }} catch (err) {{
            return {{ error: err.message || 'Unknown error' }};
        }}
    }})();
    """
    return driver.execute_script(js_code)

def get():
    # Initialize WebDriver
    driver = create_driver()
    driver.get("https://statusinvest.com.br")
    results = {}
    ivList = importIVList()['data'][:5]
    print(len(ivList))
    input('start?')
    # Loop over each ticker and fetch the corresponding data
    for asset in ivList:
        ticker = asset['symbol']
        print(f"Fetching data for: {ticker}")
        values = fetch_data_for_asset(driver, ticker)
        time.sleep(2)  # Wait a bit to make sure the data is fetched
        results[ticker] = values

    # Print the results
    input('')
    driver.quit()
    for ticker, values in results.items():
        print(f"Results for {ticker}: {values}")

if __name__ == '__main__':
    get()