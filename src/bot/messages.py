import datetime

from src.bot.handlers import bot
from src.bot.services import delete_user
from src.models import Series


def send_future_match(user_id: int, match: Series):
    message = message_future_match(match.team1_name, match.team2_name, match.tournament_name, match.date)
    sent = send_message(user_id, message)
    if not sent:
        delete_user(user_id)


def send_closest_match(user_id: int, match: Series):
    message = message_close_match(match.team1_name, match.team2_name, match.tournament_name, match.date)
    sent = send_message(user_id, message)
    if not sent:
        delete_user(user_id)


def send_result_match(user_id: int, match: Series):
    message = message_result_match(match.team1_name, match.team2_name, match.tournament_name, match.score)
    sent = send_message(user_id, message)
    if not sent:
        delete_user(user_id)


def message_future_match(team1: str, team2: str, tournament: str, date: datetime):
    return f'''
{team1} - {team2}
Турнир: {tournament}
Дата: {date} UTC
                '''


def message_close_match(team1: str, team2: str, tournament: str, date: datetime):
    return f'''
{team1} - {team2}
Турнир: {tournament}
Вот-вот начнется!
                '''


def message_result_match(team1: str, team2: str, tournament: str, score: str):
    return f'''
{team1} - {team2}
Турнир: {tournament}
Результат: {score}
                    '''


def send_message(user: int, message: str) -> bool:
    try:
        bot.send_message(user, message)
        return True
    except Exception as exc:
        return False
