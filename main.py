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
        self.urls = drom + avito + autoru
        print(self.urls)

    def send(self):
        for i in self.urls:
            time.sleep(1)
            bot.send_message(chat_id, i)

instance = BotMessage()
while True:
    instance.update()
    instance.send()
    time.sleep(60)