import telebot
from telebot import types
# import random
import requests
import json
from modules.icoModule import icoFromBytes
from modules.pngModule import pngFromBytes

global bot
supportedTypes = ['ICO', 'PNG']

try:
    settingsFile = open('./settings.json')
    settings = json.load(settingsFile)
    bot = telebot.TeleBot(settings['token'])
except OSError as ose:
    print(f'OSError:\n\t{ose}')


def get_mention(user):
    return user['user_first_name']


def stringArrayToString(arr: list, separator: str = '\n'):
    return separator.join(arr)


@bot.message_handler(commands=['start'])
def msg_preview(message: types.Message):
    bot.send_message(
        message.chat.id,
        f'Привет. Я бот, который умеет извлекать метеданные из файлов.\nПоддерживаемые типы:\n{stringArrayToString(supportedTypes)}'
    )


@bot.message_handler(
    func=lambda
    message: (
        message and
        message.document and
        message.document.mime_type == 'image/vnd.microsoft.icon'
    ),
    content_types=['document']
)
def handleIco(message: types.Message):
    file_info = bot.get_file(message.document.file_id)
    file = requests.get(
        f'https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}',
        stream=True
    )
    bot.send_message(
        message.chat.id,
        f'Вот информация о файле:\n{icoFromBytes(file.content)}'
    )


@bot.message_handler(
    func=lambda
    message: (
        message and
        message.document and
        message.document.mime_type == 'image/png'
    ),
    content_types=['document']
)
def handlePng(message: types.Message):
    file_info = bot.get_file(message.document.file_id)
    file = requests.get(
        f'https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}',
        stream=True
    )
    bot.send_message(
        message.chat.id,
        f'Вот информация о файле:\n{pngFromBytes(file.content)}'
    )


if __name__ == '__main__':
    bot.polling(none_stop=True)
