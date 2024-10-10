import asyncio
import chromadb
import os
import pandas as pd
import telebot
from dotenv import load_dotenv
from telebot import types
from telebot.async_telebot import AsyncTeleBot

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    dotenv_path
    load_dotenv(dotenv_path)
    os.environ

bot_token = os.environ['BOT-TOKEN']
bot = AsyncTeleBot(bot_token)

@bot.message_handler(commands=['start', 'help'])
async def startBot(message):
  first_mess = f"Привет, {message.from_user.first_name}!\nОпиши игру, в которую хотелось бы поиграть и я найду её!"
  await bot.send_message(message.chat.id, first_mess, parse_mode='html')

@bot.message_handler(func=lambda message: True)
async def echo_message(message):
    df_games = pd.read_csv('games.csv')
    client = chromadb.HttpClient(
        host='chromadb',
        port=8000
    )
    collection = client.get_collection(name="games")
    result = collection.query(
        query_texts=[message.text]
    )
    #ids = result['ids'][0]
    #for game_id in ids:
    #    title = df_games[df_games['app_id'] == int(game_id)]['title'].astype(str).values[0]
    print(result)
    print("test")
    await bot.send_message(message.chat.id, result)

if __name__ == "__main__":
    asyncio.run(bot.polling(restart_on_change=True))    