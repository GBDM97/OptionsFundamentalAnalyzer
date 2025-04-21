import yfinance as yf

from filesUtils import exportErrors, exportYahooAssetData, importTradingviewAssets

def generateData(index, ticker):
    data = yf.download(ticker, period="62d", interval="1d")
    market_cap = yf.Ticker(ticker).fast_info.get('marketCap')
    volatility_now = max(abs(data['High'].iloc[-1][0] - data['Low'].iloc[-2][0]), 
                             abs(data['Low'].iloc[-1][0] - data['High'].iloc[-2][0]))
    total_volatility = 0
    for i in range(0, 61):
        volatility_2d = max(abs(data['High'].iloc[-1-i][0] - data['Low'].iloc[-2-i][0]), 
                                abs(data['Low'].iloc[-1-i][0] - data['High'].iloc[-2-i][0]))
        total_volatility += volatility_2d
    avg_volatility_62d = total_volatility/62

    print(str(index) + ' ===> ' + ticker)
    return {
        'ticker': ticker,
        'volume_index': index,
        'vol_spike_ratio_2d': volatility_now/avg_volatility_62d,
        'last_price': data['Close'].iloc[-1][0],
        'market_cap': market_cap
    }

if __name__ == "__main__":
    tickers = importTradingviewAssets()[:10]
    results = []
    errors = []
    for i,v in enumerate(tickers):
        try:
            results.append(generateData(i, v))
        except Exception as error:
            errors.append(error)
            continue
    exportYahooAssetData(results)
    print(errors)
    print('Data exported!')