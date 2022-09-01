from config import config_telegram
from Request_db import get_name_serials, get_date_serial
import telebot
import time
import schedule

bot = telebot.TeleBot(config_telegram)
types = telebot.types


# def get_text():
#     bot.send_message(chat_id=1102893735, text = "Привет, прошло три секунды")

# Запрос на сериал
@bot.message_handler(commands=["get_date_serial"])
def date_serial(message):
    bot.send_message(message.chat.id, text='Введите название сериала (на русском)')
    bot.register_next_step_handler(message, release_date)


# Вывод даты выхода сериала
def release_date(message):
    name_ru_serial = message.text
    date_serials = get_date_serial(name_ru_serial)
    if date_serials == []:
        bot.send_message(message.chat.id, text='Такого сериала нет в БД')
    else:
        str_date = ''
        for serial in date_serials:
            str_date += f'{serial[0]:10}{serial[1]}\n'
        str_date = str_date.strip('\n')
        bot.send_message(message.chat.id, text=f'Выход серий:\n{str_date}')


# Запрос названия сериала
@bot.message_handler(commands=["get_name_serials"])
def get_text_messages(message):
    name_serials = get_name_serials()
    str_name = ''
    for name_serial in name_serials:
        str_name += name_serial[0] + '\n'
    str_name = str_name.strip('\n')
    bot.send_message(message.chat.id, text=f'Сериалы в базе данных:\n{str_name}')


@bot.message_handler(content_types=['text'])
def return_answer(message):
    bot.send_message(message.chat.id, text='Не знаю, что делать')


# schedule.every(3).seconds.do(get_text)
# while True:
#     schedule.run_pending()
#     time.sleep(1)
bot.polling(none_stop=True, interval=0)
