"""
Module that implements Telegram bot api
"""
import time

import telebot
from config import TG_TOKEN

bot = telebot.TeleBot(TG_TOKEN)
chat_id = "@lowcostparser"
import drom_parser
import avito_parser
import auto_ru_parser
import os
import avito_parser_cars

class BotMessage:
    """
    Collects media files and sends them to the chat
    """

    def __init__(self):
        pass

    def update(self):
        drom = drom_parser.get_links()
        avito = avito_parser.get_links()
        autoru = auto_ru_parser.get_links()
        avito_car = avito.get_links()
        print(avito)
        self.urls = avito + drom + autoru + avito_car
        if not self.check_file():
            self.send()

    def send(self):
        bot.send_message(chat_id, "Новая подборка")
        bot.send_message(chat_id, '\n'.join(self.urls))

    def check_file(self):
        if os.path.exists('urls.txt'):
            with open('urls.txt', 'rt') as file:
                files_url = []
                for f in file.readlines():
                    files_url.append(f.strip())
            return files_url == self.urls
        with open('urls.txt', 'wt') as file:
            for url in self.urls:
                file.write(url+'\n')
        return False

instance = BotMessage()
while True:
    instance.update()
    time.sleep(30)