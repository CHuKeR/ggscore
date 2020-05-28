import telebot
from telebot import apihelper
from telebot import types

from src.api.models import Users, Teams
from src.bot.buttons import (
    add_team_button,
    add_row_next_previous,
    add_new_teams_button,
    delete_teams_button,
    callback_button_exit,
    delete_team_button
)
from src.config import config
from src.extensions import session

bot = telebot.TeleBot(config.BOT_API_TOKEN)


@bot.message_handler(commands=["start"])
def start(message):
    user = session.query(Users).filter(Users.id == message.chat.id).first()
    if user is None:
        session.add(Users(id=message.chat.id))
        session.commit()
    bot.send_message(message.from_user.id, 'Team Spirit <3')


@bot.message_handler(commands=["setting"])
def settings(message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(add_new_teams_button(0), delete_teams_button(0))
    keyboard.add(callback_button_exit)
    bot.send_message(chat_id=message.chat.id, text="Выберите настройку:", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == "close_settings")
def back_to_start(call):
    if call.message:
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


@bot.callback_query_handler(func=lambda call: True and call.data.startswith("add_teams"))
def add_teams(call):
    if call.message:
        page = int(call.data.split('_')[-1])
        keyboard = types.InlineKeyboardMarkup()
        teams = session.query(Teams) \
            .filter(~Teams.users.any(Users.id == call.from_user.id)) \
            .limit(10) \
            .offset(page * 10).all()
        teams_count = session.query(Teams).count()
        for team in teams:
            keyboard.add(add_team_button(team.name, team.id))
        add_row_next_previous(page, 'add', keyboard, teams_count)
        keyboard.add(callback_button_exit)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Выберите команду:", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True and call.data.startswith("add_"))
def add_team(call):
    if call.message:
        team_id = int(call.data.split('_')[-1])
        user = session.query(Users).filter(Users.id == call.from_user.id).first()
        team = session.query(Teams).filter(Teams.id == team_id).first()
        user.teams.append(team)
        session.commit()
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(add_new_teams_button(0), delete_teams_button(0))
    keyboard.add(callback_button_exit)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Команда добавлена! Выберите дальнейшее действие:", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True and call.data.startswith("delete_teams"))
def delete_teams(call):
    if call.message:
        page = int(call.data.split('_')[-1])
        keyboard = types.InlineKeyboardMarkup()
        teams = session.query(Teams) \
            .filter(Teams.users.any(Users.id == call.from_user.id)) \
            .limit(10) \
            .offset(page * 10).all()
        teams_count = session.query(Teams).count()
        for team in teams:
            keyboard.add(delete_team_button(team.name, team.id))
        add_row_next_previous(page, 'delete', keyboard, teams_count)
        keyboard.add(callback_button_exit)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Выберите команду:", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True and call.data.startswith("delete_"))
def delete_team(call):
    if call.message:
        team_id = int(call.data.split('_')[-1])
        user = session.query(Users).filter(Users.id == call.from_user.id).first()
        team = session.query(Teams).filter(Teams.id == team_id).first()
        user.teams.remove(team)
        session.commit()
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(add_new_teams_button(0), delete_teams_button(0))
    keyboard.add(callback_button_exit)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Команда удалена! Выберите дальнейшее действие:", reply_markup=keyboard)
