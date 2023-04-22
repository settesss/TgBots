import requests
import random
import telebot
import config
from bs4 import BeautifulSoup as bs

START_COMMAND = 'Добро пожаловать в Wooord Hunt! Для нового слова введите любую цифру!'

HELP_COMMAND = """
Привет! Я бот для работы с словарями Wooord Hunt.
Чтобы начать работу, напишите /start.
Для помощи, напишите /help."""

URL = 'https://wooordhunt.ru/dic/list/en_ru/ab'


def parser(url):
    r = requests.get(url)
    soup = bs(r.text, 'html.parser')
    dictionary = soup.find_all('p')
    return [c.text for c in dictionary]


list_of_words = parser(URL)
random.shuffle(list_of_words)
bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def handle_start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    user_markup.row('Изучать слова', 'Мои ошибки')
    user_markup.row('Награды')
    user_markup.row('Помощь')
    user_markup.row('Записаться на урок')
    bot.send_message(message.chat.id, START_COMMAND, reply_markup=user_markup)
    bot.delete_message(message.chat.id, message.message_id)


@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.reply_to(message, HELP_COMMAND)
    bot.delete_message(message.chat.id, message.message_id)


@bot.message_handler(content_types=['text'])
def words(message):
    if message.text.lower() in '123456789':
        bot.send_message(message.chat.id, list_of_words[0])
        del list_of_words[0]
    else:
        bot.send_message(message.chat.id, 'Цифру!')


bot.polling()