from telebot import types

from src.bot.buttons import (
    add_team_button,
    delete_team_button,
    next_page_button,
    previous_page_button,
    add_new_teams_button,
    delete_teams_button,
    callback_button_exit
)
from src.extensions import session
from src.models import Users, Teams


def add_user(user_id: int):
    user = session.query(Users).filter(Users.id == user_id).first()
    if user is None:
        session.add(Users(id=user_id))
        session.commit()


def get_settings_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(add_new_teams_button(0), delete_teams_button(0))
    keyboard.add(callback_button_exit)
    return keyboard


def get_add_teams_keyboard(message: str, user_id: int):
    page = int(message.split('_')[-1])
    keyboard = types.InlineKeyboardMarkup()
    teams = session.query(Teams) \
        .filter(~Teams.users.any(Users.id == user_id)) \
        .limit(10) \
        .offset(page * 10).all()
    teams_count = session.query(Teams).count()
    for team in teams:
        keyboard.add(add_team_button(team.name, team.id))
    add_row_next_previous(page, 'add', keyboard, teams_count)
    keyboard.add(callback_button_exit)
    return keyboard


def add_team(message: str, user_id: int):
    team_id = int(message.split('_')[-1])
    user = session.query(Users).filter(Users.id == user_id).first()
    team = session.query(Teams).filter(Teams.id == team_id).first()
    user.teams.append(team)
    session.commit()


def get_delete_teams_keyboard(message: str, user_id: int):
    page = int(message.split('_')[-1])
    keyboard = types.InlineKeyboardMarkup()
    teams = session.query(Teams) \
        .filter(Teams.users.any(Users.id == user_id)) \
        .limit(10) \
        .offset(page * 10).all()
    teams_count = session.query(Teams).count()
    for team in teams:
        keyboard.add(delete_team_button(team.name, team.id))
    add_row_next_previous(page, 'delete', keyboard, teams_count)
    keyboard.add(callback_button_exit)
    return keyboard


def add_row_next_previous(page: int, action_type: str, keyboard: types.InlineKeyboardMarkup, count: int):
    next_page = next_page_button(page, action_type)
    prev_page = previous_page_button(page, action_type, count)
    if next_page and prev_page:
        keyboard.row(next_page, prev_page)
    elif next_page and not prev_page:
        keyboard.row(next_page)
    elif not next_page and prev_page:
        keyboard.row(prev_page)
    else:
        pass


def delete_team(message: str, user_id: int):
    team_id = int(message.split('_')[-1])
    user = session.query(Users).filter(Users.id == user_id).first()
    team = session.query(Teams).filter(Teams.id == team_id).first()
    user.teams.remove(team)
    session.commit()
