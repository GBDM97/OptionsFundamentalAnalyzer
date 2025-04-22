import json
import pandas as pd

def fromJson():
    with open('data\\output.json') as file:
        data = json.loads(file.read())
        df = pd.DataFrame(data, columns=['ASSET', 'VOLUME INDEX', 'VOLATILITY SPIKE RATIO', 'LAST PRICE', 'MARKET CAP'])
        df.to_excel('data\\output.xlsx', index=False)

fromJson()