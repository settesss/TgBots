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


def ask_question(chat_id):
    global row_number, question_word, answer_word
    row_number = str(random.randrange(1, SHEET_ROWS_COUNT))
    question_word = sheet['A' + row_number].value
    answer_word = sheet['B' + row_number].value
    other_words = [sheet['B' + str(i)].value for i in range(1, SHEET_ROWS_COUNT) if
                   i != row_number]
    other_words_sampled = random.sample(other_words, 3)
    answer_cells = [answer_word] + other_words_sampled
    random.shuffle(answer_cells)
    answer_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    answer_markup.row(answer_cells[0], answer_cells[1])
    answer_markup.row(answer_cells[2], answer_cells[3])
    answer_markup.row("Я устал ⛔")
    bot.send_message(chat_id, question_word.title(), reply_markup=answer_markup)
    del question_word


@bot.message_handler(content_types=['text'])
def echo(message):
    if message.text.lower() == 'изучать слова 📖':
        bot.send_message(message.chat.id, "Поехали!")
        ask_question(message.chat.id)
    elif message.text.lower() == answer_word:
        bot.send_message(message.chat.id, "Молодец!")
        ask_question(message.chat.id)
    elif message.text.lower() == 'Я устал ⛔'.lower():
        bot.send_message(message.chat.id, "Спасибо за завершение работы!")
        handle_start(message)
    else:
        bot.send_message(message.chat.id, "Не молодец!")
        ask_question(message.chat.id)


bot.polling()
