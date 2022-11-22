import telebot
import config
import parser
import time
import datetime

bot = telebot.TeleBot(config.BOT_TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(commands=['timer'])
def timer(message):
    print(message.chat.id)
    print(message)
    n = 5
    time.sleep(n)
    bot.reply_to(message, f'Прошло {n} секунд{message.id}')


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    print(message.chat.id)
    # print(message)
    print(message.text + ' - ' + message.from_user.username + " - " + datetime.datetime.now().strftime("%H:%M:%S"))
    if message.text[0] == '/':
        bot.reply_to(message, 'command unknown')

    else:
        bot.reply_to(message, 'howdy?')


if __name__ == '__main__':
    bot.infinity_polling()
