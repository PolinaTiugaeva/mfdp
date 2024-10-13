import os
import json
import pandas as pd
import telebot
from dotenv import load_dotenv
from loguru import logger
from telebot.util import quick_markup
from database.containers import Container
from database.database import get_collection, get_session, init_db
from models.history import History
from services.crud.history import add_to_history


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    dotenv_path
    load_dotenv(dotenv_path)
    os.environ

bot_token = os.environ['BOT_TOKEN']
bot = telebot.TeleBot(bot_token)

df_games = pd.read_csv('games.csv')

@bot.message_handler(commands=['start', 'help'])
def startBot(message):
    first_mess = f"Привет, {message.from_user.first_name}!\nОпиши игру, в которую хотелось бы поиграть и я найду её!"
    bot.send_message(message.chat.id, first_mess, parse_mode='html')


@bot.message_handler(func=lambda message: True)
def game_searching(message):
    collection = get_collection()
    result = collection.query(
        query_texts=[message.text]
    )
    markup = quick_markup({
        '\U0001F44D': {'callback_data': "1"},
        '\U0001F44E': {'callback_data': "0"}
    }, row_width=2)
    ids = result['ids'][0]
    for game_id in ids:
        title = df_games[df_games['app_id'] == int(game_id)]['title'].astype(str).values[0]
        bot.send_message(message.chat.id, title, reply_markup=markup)



@bot.callback_query_handler(func=lambda call: True)
def reaction_callback(call): 
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