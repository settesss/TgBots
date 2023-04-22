import random
import telebot
import config
from openpyxl import load_workbook

START_COMMAND = 'Добро пожаловать в Wooord Hunt!'

HELP_COMMAND = """
Привет! Я бот для работы с словарями Wooord Hunt.
Чтобы начать работу, напишите /start.
Для помощи, напишите /help."""

book = load_workbook(filename="D:/words.xlsx")
sheet = book['Лист1']
SHEET_ROWS_COUNT = sheet.max_row
row_number = None
question_word = None
answer_word = None

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def handle_start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    user_markup.row('Изучать слова 📖', 'Мои ошибки ⚠️')
    user_markup.row('Награды 🥇')
    user_markup.row('Помощь 🆘')
    user_markup.row('Записаться на урок 💎')
    bot.send_message(message.chat.id, START_COMMAND, reply_markup=user_markup)
    bot.delete_message(message.chat.id, message.message_id)


@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.reply_to(message, HELP_COMMAND)
    bot.delete_message(message.chat.id, message.message_id)


@bot.message_handler(content_types=['text'])
def echo(message):
    global row_number, question_word, answer_word
    if message.text.lower() == 'изучать слова 📖':
        bot.send_message(message.chat.id, "Поехали!")
        row_number = str(random.randrange(1, SHEET_ROWS_COUNT))
        question_word = sheet['A' + row_number].value
        answer_word = sheet['B' + row_number].value
        answer_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        answer_markup.row(sheet['B' + str(random.randrange(1, SHEET_ROWS_COUNT))].value,
                          sheet['B' + str(random.randrange(1, SHEET_ROWS_COUNT))].value)
        answer_markup.row(sheet['B' + str(random.randrange(1, SHEET_ROWS_COUNT))].value,
                          answer_word)
        bot.send_message(message.chat.id, question_word.title(), reply_markup=answer_markup)
    elif message.text.lower() == answer_word.lower():
        bot.send_message(message.chat.id, "Молодец!")
        row_number = str(random.randrange(1, SHEET_ROWS_COUNT))
        question_word = sheet['A' + row_number].value
        answer_word = sheet['B' + row_number].value
        answer_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        answer_markup.row(sheet['B' + str(random.randrange(1, SHEET_ROWS_COUNT))].value,
                          sheet['B' + str(random.randrange(1, SHEET_ROWS_COUNT))].value)
        answer_markup.row(sheet['B' + str(random.randrange(1, SHEET_ROWS_COUNT))].value,
                          answer_word)
        bot.send_message(message.chat.id, question_word.title(), reply_markup=answer_markup)
    else:
        bot.send_message(message.chat.id, "Не молодец!")
        row_number = str(random.randrange(1, SHEET_ROWS_COUNT))
        question_word = sheet['A' + row_number].value
        answer_word = sheet['B' + row_number].value
        answer_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        answer_markup.row(sheet['B' + str(random.randrange(1, SHEET_ROWS_COUNT))].value,
                          sheet['B' + str(random.randrange(1, SHEET_ROWS_COUNT))].value)
        answer_markup.row(sheet['B' + str(random.randrange(1, SHEET_ROWS_COUNT))].value,
                          answer_word)
        bot.send_message(message.chat.id, question_word.title(), reply_markup=answer_markup)
    del question_word


bot.polling()
