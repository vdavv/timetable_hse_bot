import json
import telebot
from telebot import TeleBot
import config
import time
import datetime as dt
from datetime import datetime
import parser

# import heapq

bot: TeleBot = telebot.TeleBot(config.BOT_TOKEN)

markup = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
button1 = telebot.types.KeyboardButton('Get Timetable')
markup.add(button1)


def print_in_terminal(message):
    print(message.chat.id)
    # print(message)
    print(message.text + ' - ' + message.from_user.username + " - " + dt.datetime.now().strftime("%H:%M:%S"))


def create_out_string(json_file):
    to_return_common = ''
    to_return_first = ''
    to_return_second = ''
    lessons_list = json_file['data']
    date = lessons_list[0]["date"]
    to_return_common += '🟥 ' + lessons_list[0]["dayOfWeekString"] + ' '
    to_return_common += date[-1:-3:-1][::-1] + '/' + date[-4:-6:-1][::-1] + ':\n\n'


def read_timetable(json_file):
    # 🔴 🟥
    to_return = ''
    lessons_list = json_file['data']
    date = lessons_list[0]["date"]
    to_return += '🟥 ' + lessons_list[0]["dayOfWeekString"] + ' '
    to_return += date[-1:-3:-1][::-1] + '/' + date[-4:-6:-1][::-1] + ':\n\n'
    num = 0
    for lesson in lessons_list:
        if date != lesson['date']:
            num += 1
            if num >= 1:
                break
            date = lesson['date']
            to_return += lesson["dayOfWeekString"] + ' '
            to_return += lesson['date'][-1:-3:-1][::-1] + '/' + lesson['date'][-4:-6:-1][::-1] + ':\n\n'
            to_return += str(lesson["lessonNumberStart"])
            to_return += ' - '
            to_return += lesson["auditorium"] + ' '
            to_return += lesson["discipline"] + ' '
            to_return += lesson["beginLesson"] + '-' + lesson["endLesson"]
            to_return += '\n\n'
        else:
            to_return += str(lesson["lessonNumberStart"])
            to_return += ' - '
            to_return += lesson["auditorium"] + ' '
            to_return += lesson["discipline"] + ' '
            to_return += lesson["beginLesson"] + '-' + lesson["endLesson"]
            to_return += '\n\n'

    return to_return


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "This is bot for retrieving FCS HSE timetable", reply_markup=markup)


@bot.message_handler(commands=['timer'])
def timer(message):
    print(message.chat.id)
    print(message)
    n = 5
    time.sleep(n)
    bot.reply_to(message, f'Прошло {n} секунд {message.id}')


"""@bot.message_handler(func=lambda message: True)
def echo_all(message):
    print(message.chat.id)
    # print(message)
    print(message.text + ' - ' + message.from_user.username + " - " + dt.datetime.now().strftime("%H:%M:%S"))
    if message.text[0] == '/':
        bot.reply_to(message, 'command unknown')

    else:
        pass
        if dt.datetime.now().strftime("%H") in ['1', '7', '13', '19']:
            pass
            # update timetable
        bot.reply_to(message, 'under development')"""


@bot.message_handler(func=lambda message: message.text == 'Get Timetable')
def send_timetable(message):
    print_in_terminal(message)
    today_v = datetime.today()
    today_plus7_v = (dt.datetime.now() + dt.timedelta(days=1))
    parser.get_schedule_by_group('129742', today_v, today_plus7_v.strftime('%Y-%m-%d'))
    flag = True
    while flag:
        try:
            with open(f'data/data_{today_v.strftime("%Y_%m_%d_%H%M")}.json', 'r') as openfile:
                flag = False
        except:
            time.sleep(1)
    with open(f'data/data_{today_v.strftime("%Y_%m_%d_%H%M")}.json', 'r') as openfile:
        # Reading from json file
        json_timetable = json.load(openfile)
    bot.reply_to(message, read_timetable(json_timetable))


@bot.message_handler(func=lambda message: message.text in config.terminate_phrases)
def terminate_bot(message):
    print_in_terminal(message)
    bot.reply_to(message, 'bot terminated')
    bot.stop_bot()


"""while True:
    if dt.datetime.now().strftime("%H") in ['1', '7', '13', '19']:
        pass
        # send timetable
    time.sleep(60)"""

if __name__ == '__main__':
    bot.infinity_polling()
