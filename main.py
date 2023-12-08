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
    diff= percentage_difference(data[item1][1], data[item2][1])
    msg= f'Brecha {item1} {data[item1][1]} / {item2} {data[item2][1]}: Brecha {diff}%'    
    print(msg)
    if diff > 5:
        asyncio.run(telegramear(msg))

def market_closed():
    return not (config.start_time <= datetime.datetime.now().time() <= config.end_time)
        
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




def get_element(url, element):
    try:
        # Send an HTTP request to the website
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad requests
        
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Locate the element by its id
        desired_element = soup.find(class_=element).find('p').text.strip()
        print(desired_element)

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None


url = 'https://www.dolarito.ar'
response = requests.get(url)

# Create a BeautifulSoup object
soup = BeautifulSoup(response.text, 'html.parser')

# Find specific elements on the page
title = soup.title.text
#paragraphs = soup.find_all('p')
fichas = soup.find_all(class_='chakra-wrap__listitem')

# Print the results
data= {  
    'OFICIAL': extract(0, fichas),
    'BLUE': extract(1, fichas),
    'MEP': extract(6, fichas),
    'CRYPTO': extract(11, fichas),
}

print(data)
save_data(data)
check_spread('BLUE','MEP',data)
check_spread('BLUE','CRYPTO',data)
