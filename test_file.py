import SQLighter
import telebot
import config
from telebot import types
import dota_parser_lib as dpl


bot = telebot.TeleBot("421285495:AAGd1N4zW2UuWWajsswD-QYkLaKdLGHp8pk")
sqler = SQLighter.DotaSqlClient()


@bot.message_handler(commands=["start"])
def add_user_id(message):
    keyboard = types.InlineKeyboardMarkup()
    callback_button1 = types.InlineKeyboardButton(text="Получить матчи на сегодня!", callback_data="today")
    callback_button2 = types.InlineKeyboardButton(text="Настройки", callback_data="setting")
    keyboard.add(callback_button1,callback_button2)
    bot.send_message(message.chat.id,"Выберите действие:", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True and call.data == "setting")
def callback_inline(call):
    if call.message:
        keyboard = types.InlineKeyboardMarkup()
        callback_button1 = types.InlineKeyboardButton(text="Настройка выбора команд", callback_data="settigs_teams")
        callback_button2 = types.InlineKeyboardButton(text="Настройки вывода результата матча", callback_data="settigs_results")
        keyboard.add(callback_button1, callback_button2)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text ="Выберите настройку:", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True and call.data[7:]== "setting_")
def callback_inline(call):
    if call.message:
        keyboard = types.InlineKeyboardMarkup()
        callback_button1 = types.InlineKeyboardButton(text="Настройка выбора команд", callback_data="settigs_teams")
        callback_button2 = types.InlineKeyboardButton(text="Настройки вывода результата матча", callback_data="settigs_results")
        keyboard.add(callback_button1, callback_button2)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = "Выберите настройку:", reply_markup=keyboard)


if __name__ == '__main__':
    bot.remove_webhook()
    bot.polling(none_stop=True)
