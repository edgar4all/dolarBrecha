import requests
url = 'https://api.binance.com/api/v3/ticker/price'

symbol = 'USDTARS'

params = {'symbol': symbol}

response = requests.get(url, params=params)

if response.status_code == 200:    
    data = response.json()    
    current_price = data.get('price')    
    print(f'Precio actual {symbol}: { round(float(current_price),2) }')
else:
    print(f'Error: Unable to fetch data. Status code: {response.status_code}')
    print(response.text)