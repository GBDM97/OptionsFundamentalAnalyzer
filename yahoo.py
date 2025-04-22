import yfinance as yf

from filesUtils import exportErrors, exportYahooAssetData, importTradingviewAssets

def generateData(index, ticker):
    data = yf.download(ticker, period="62d", interval="1d")
    volatility_now = max(abs(data['High'].iloc[-1][0] - data['Low'].iloc[-2][0]), 
                             abs(data['Low'].iloc[-1][0] - data['High'].iloc[-2][0]))
    total_volatility = 0
    for i in range(0, 61):
        volatility_2d = max(abs(data['High'].iloc[-1-i][0] - data['Low'].iloc[-2-i][0]), 
                                abs(data['Low'].iloc[-1-i][0] - data['High'].iloc[-2-i][0]))
        total_volatility += volatility_2d
    avg_volatility_62d = total_volatility/62

    print(str(index) + ' ===> ' + ticker)
    spike_ratio = volatility_now/avg_volatility_62d
    if spike_ratio < 1:
        return None
    return [
        ticker,
        index+1,
        spike_ratio,
        data['Close'].iloc[-1][0]
    ]

if __name__ == "__main__":
    tickers = importTradingviewAssets()
    results = []
    errors = []
    for i,v in enumerate(tickers):
        try:
            result = generateData(i, v)
            if result:
                results.append(result)
        except Exception as error:
            errors.append(error)
            continue
    exportYahooAssetData(results)
    print(errors)
    print('Data exported!')