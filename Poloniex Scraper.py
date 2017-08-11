from tqdm import tqdm
import requests
import csv
import json

r = requests.get('https://poloniex.com/public?command=returnCurrencies')

data = json.loads(r.content)
exname = data.keys()
goodones = []

#Get Rid of All currencies that are not Active
for ex in exname:
    if (data[ex]['delisted'] == 0 and data[ex]['disabled'] == 0):
        goodones.append(ex)

for name in tqdm(goodones):

    csvfile = open(name + '.csv', 'wb')
    fieldnames = ['date', 'high', 'low', 'open', 'close', 'volume', 'quoteVolume', 'weightedAverage']
    linkwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
    r = requests.get(
        'https://poloniex.com/public?command=returnChartData&currencyPair=BTC_' + name + '&start=1281466382&end=9999999999&period=14400')
    data = r.content
    data = json.loads(data)
    linkwriter.writeheader()
    for row in data:
        try:
            linkwriter.writerow(row)
        except:
            print(name +' Failed')
            pass
    csvfile.close()

