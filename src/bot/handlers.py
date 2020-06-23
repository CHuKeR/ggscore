import telebot
from telebot import apihelper

from src.bot.services import add_user, get_settings_keyboard, get_add_teams_keyboard, add_team, \
    get_delete_teams_keyboard, delete_team
from src.config import config

bot = telebot.TeleBot(config.BOT_API_TOKEN)

if config.DEBUG:
    apihelper.proxy = {'https': 'socks5://localhost:9050'}


@bot.message_handler(commands=["start"])
def start_handler(message):
    user_id = message.from_user.id
    add_user(user_id)
    bot.send_message(user_id, 'Team Spirit <3. Ах да, настройки. Воспользуйтесь командой /setting')


@bot.message_handler(commands=["setting"])
def settings_handler(message):
    keyboard = get_settings_keyboard()
    bot.send_message(chat_id=message.chat.id, text="Выберите настройку:", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == "close_settings")
def back_to_start_handler(call):
    if call.message:
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


@bot.callback_query_handler(func=lambda call: True and call.data.startswith("add_teams"))
def add_teams_handler(call):
    if call.message:
        message = call.data
        user_id = call.from_user.id
        keyboard = get_add_teams_keyboard(message, user_id)
        bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                              text="Выберите команду:", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True and call.data.startswith("add_"))
def add_team_handler(call):
    if call.message:
        message = call.data
        user_id = call.from_user.id
        add_team(message, user_id)
        keyboard = get_settings_keyboard()
        bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                              text="Команда добавлена! Выберите дальнейшее действие:", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True and call.data.startswith("delete_teams"))
def delete_teams_handler(call):
    if call.message:
        message = call.data
        user_id = call.from_user.id
        keyboard = get_delete_teams_keyboard(message, user_id)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Выберите команду:", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True and call.data.startswith("delete_"))
def delete_team_handler(call):
    if call.message:
        message = call.data
        user_id = call.from_user.id
        delete_team(message, user_id)
        keyboard = get_settings_keyboard()
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Команда удалена! Выберите дальнейшее действие:", reply_markup=keyboard)
