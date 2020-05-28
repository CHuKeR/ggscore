import telebot
from telebot import apihelper

from src.config import config

apihelper.proxy = {'https': 'socks5://localhost:9050'}

bot = telebot.TeleBot(config.BOT_API_TOKEN)
