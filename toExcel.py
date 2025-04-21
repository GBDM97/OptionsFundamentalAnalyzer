import json
import pandas as pd

def fromJson():
    with open('data\\output.json') as file:
        data = json.loads(file.read())
        df = pd.DataFrame(data, columns=['ASSET', 'VOLUME', 'PRICE'])
        df.to_excel('data\\output.xlsx', index=False)

fromJson()