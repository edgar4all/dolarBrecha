Este proyecto necesita que generes tu propio archivo de configuración.

----config.py:----

#Este es el contenido de la config... =)
import datetime

#Configurar si queres recibir las alertas por telegram.
TOKEN_BOT = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
TELEGRAM_CHAT_ID = "XXXXXXXXX"

dbhost='localhost'
dbuser='root'
dbpassword=''
database='dolarbrecha'

#Horario del mercado
market_starts = datetime.time(10, 0, 0)  # 10:00:00 AM
market_ends = datetime.time(18, 0, 0)  # 6:00:00 PM

#fin del archivo de configuracion
