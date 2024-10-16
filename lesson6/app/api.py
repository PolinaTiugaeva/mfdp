import os
import pika
import json
import telebot

from dotenv import load_dotenv
from loguru import logger
from telebot.util import quick_markup

from database.containers import Container
from database.database import get_session, init_db, get_chanel
from models.history import History
from services.crud.history import add_to_history


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    dotenv_path
    load_dotenv(dotenv_path)
    os.environ

bot_token = os.environ['BOT_TOKEN']
bot = telebot.TeleBot(bot_token)

@bot.message_handler(commands=['start', 'help'])
def startBot(message):
    first_mess = f"Привет, {message.from_user.first_name}!\nОпиши игру, в которую хотелось бы поиграть и я найду её!"
    logger.info(message.chat.id)
    logger.info(message)
    bot.send_message(message.chat.id, first_mess, parse_mode='html')

@bot.message_handler(func=lambda message: True)
def game_searching_req(message):
    logger.info(f'message - {message}')
    body = json.dumps({
        'username' : message.from_user.username,
        'chat_id' : message.chat.id,
        'text' : message.text
    })
    logger.info(f'body - {body}')
    chanel = get_chanel()
    chanel.basic_publish(
        exchange='',
        routing_key='search_request',
        body=body,
        properties=pika.BasicProperties(
            delivery_mode=2
        )
    )
    chanel.basic_ack()


@bot.callback_query_handler(func=lambda call: True)
def reaction_callback(call): 
    logger.info("!!!!!!!!!!!!!!!!!!!!!!!!")
    session = get_session()
    new_item = History(
        username = call.from_user.username,
        game_title = call.message.text,
        reaction = call.json['data']
    )
    add_to_history(new_item, session)


if __name__ == "__main__":
    container = Container()
    container.init_resources()
    container.wire(modules=[__name__], packages=["database"])
    #init_db()
    logger.info("Start bot")
    bot.infinity_polling()