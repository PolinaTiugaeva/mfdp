import asyncio
import chromadb
import os
import pandas as pd
import telebot
from dotenv import load_dotenv
from telebot import types
from telebot import TeleBot

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    dotenv_path
    load_dotenv(dotenv_path)
    os.environ

bot_token = os.environ['BOT-TOKEN']
bot = TeleBot(bot_token)

df_games = pd.read_csv('games.csv')
client = chromadb.HttpClient(
    host='chromadb',
    port=8000
)
collection = client.get_collection(name="games")

@bot.message_handler(commands=['start', 'help'])
def startBot(message):
    first_mess = f"Привет, {message.from_user.first_name}!\nОпиши игру, в которую хотелось бы поиграть и я найду её!"
    bot.send_message(message.chat.id, first_mess, parse_mode='html')

@bot.message_handler(func=lambda message: True)
def game_searching(message):
    result = collection.query(
        query_texts=[message.text]
    )
    ids = result['ids'][0]
    for game_id in ids:
        title = df_games[df_games['app_id'] == int(game_id)]['title'].astype(str).values[0]
        bot.send_message(message.chat.id, title)

if __name__ == "__main__":
    bot.infinity_polling(restart_on_change=True)