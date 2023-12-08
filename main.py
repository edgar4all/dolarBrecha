import requests 
from bs4 import BeautifulSoup
import config
from telegram import Bot
import asyncio
import sys
import datetime
import mysql.connector

def extract(index,fichas):
    precios= fichas[index].find_all(class_=['css-12u0t8b']) 
    #precio_compra= float(precios[0].text.replace(',', '.'))
    print(precios)
    precio_venta = float(precios[0].text.replace(',', '.'))
    return [ 0, precio_venta ]

def percentage_difference(a, b):
    difference = a - b
    percentage_difference = (difference / a) * 100
    return round(percentage_difference ,1)

async def telegramear(msg):    
    bot = Bot(token=config.TOKEN_BOT)
    await bot.send_message(chat_id=config.TELEGRAM_CHAT_ID, text=msg)

def check_spread(item1,item2,data):
    diff= percentage_difference(data[item1], data[item2])
    msg= f'Brecha {item1} {data[item1]} / {item2} {data[item2]}: Brecha {diff}%'    
    print(msg)
    if diff > 5:
        asyncio.run(telegramear(msg))

def market_closed():
    return not (config.market_starts <= datetime.datetime.now().time() <= config.market_ends)
        
def save_data(data):
    try:

        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        conn = mysql.connector.connect(host=config.dbhost,user=config.dbuser,password=config.dbpassword,database=config.database)
        #conn = config.conn
        cursor= conn.cursor()
        for key, value in data.items():
            sql= "INSERT INTO dolar(nombre,compra,venta,fecha) VALUES (%s,%s,%s,%s)"
            sql_data = (key, value[0],value[1], now)

            cursor.execute(sql, sql_data)
            conn.commit()

        cursor.close()
        conn.close()
    except Exception as error:
        print("DB Error: ", error)

############################################################

#if market_closed(): sys.exit()


def get_cotizacion(url):
    try:        
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad requests
        
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')        
        cotizacion = soup.find(class_="data__valores").find('p').contents[0]
        return float(cotizacion)

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

# Example usage
url= 'https://dolarhoy.com/i/cotizaciones/'

data= {  
    'OFICIAL': get_cotizacion(url+'dolar-bancos-y-casas-de-cambio'),
    'BLUE': get_cotizacion(url+'dolar-blue'),
    'MEP': get_cotizacion(url+'dolar-mep'),
    'CCL': get_cotizacion(url+'dolar-contado-con-liquidacion'),
    #'CRYPTO': get_cotizacion(url+'bitcoin-usd'),
}

print(data)
#save_data(data)
check_spread('BLUE','MEP',data)
check_spread('BLUE','OFICIAL',data)
check_spread('BLUE','CCL',data)
