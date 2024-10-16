import os
import pika
import json
import telebot

from dotenv import load_dotenv
from loguru import logger
from telebot.util import quick_markup

from database.containers import Container
from database.database import get_chanel, get_bot_token

container = Container()
container.init_resources()

def process_request(ch, method, properties, body):
    logger.info(f'body - {body}')
    message = json.loads(body)
    logger.info(f'message - {message}')
    sorted_game_scores = sorted(message['game_scores'], key= lambda x: x[1], reverse=True)
    bot = telebot.TeleBot(get_bot_token())
    markup = quick_markup({
        '\U0001F44D': {'callback_data': "1"},
        '\U0001F44E': {'callback_data': "0"}
    }, row_width=2)
    for game_score in sorted_game_scores:
        bot.send_message(message['chat_id'], text=game_score[0], reply_markup=markup)
    ch.basic_ack(delivery_tag=method.delivery_tag)
    

if __name__ == "__main__":
    container.wire(modules=[__name__], packages=["database"])
    #init_db()
    chanel = get_chanel()
    chanel.queue_declare(queue='notify_queue', durable=True)
    chanel.basic_consume(queue='notify_queue', on_message_callback=process_request)
    logger.info("Start consumption")
    chanel.start_consuming()