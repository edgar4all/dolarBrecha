import config
from telegram import Bot

bot = Bot(token=config.TOKEN_BOT)
bot.send_message(chat_id=config.TELEGRAM_CHAT_ID, text="Alerta Brecha de Dolar")


