import configparser
import logging

# pip install pyTelegramBotAPI
import telebot
from telebot import types

from db_manager import DBManager

# прочитать Токен из конфига
config = configparser.ConfigParser()
config.read('telebot_config.ini')
token = config['telebot']['token']
bot = telebot.TeleBot(token)  # @db_manager_bot

db_manager = DBManager()

crud_options = ['Создание', 'Чтение', 'Изменение', 'Удаление']


@bot.message_handler(commands=['start'])
def new_game(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}!')

    crud_markup = types.InlineKeyboardMarkup([[types.InlineKeyboardButton(text=option, callback_data=f'crud_{i}')
                                              for i, option
                                              in enumerate(crud_options)]])
    bot.send_message(message.chat.id,
                     "Выбери тип действия с базой данных",
                     reply_markup=crud_markup)


@bot.callback_query_handler(func=lambda call: "crud_" in call.data)
def crud_query_handler(call):
    call_data_split = call.data.split('_')
    if len(call_data_split) < 2 or not call_data_split[1].isdigit():
        bot.send_message(call.message.chat.id,
                         'Что-то пошло не так!\nПопробуй перезагрузить сессию /start')
    else:
        option_id = int(call_data_split[1])
        bot.answer_callback_query(callback_query_id=call.id,
                                  text="Отличный выбор!")

        bot.send_message(call.message.chat.id,
                         "Выбери запрос из списка")

        ask_to_chose_query_by_typeid(option_id, call.message)


def ask_to_chose_query_by_typeid(option_id, message):
    ...


if __name__ == '__main__':
    # настройка логирования
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )

    # load_statistics()

    logging.info('Starting the bot...')
    bot.polling(none_stop=True, interval=0)
    logging.info('The bot has stopped!')
