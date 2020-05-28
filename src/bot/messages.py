import datetime

from src.api.models import Series
from src.bot import bot


def send_future_match(user: id, match: Series):
    message = message_future_match(match.team1_name, match.team2_name, match.tournament_name, match.date)
    bot.send_message(user, message)


def send_result_match(user: id, match: Series):
    message = message_result_match(match.team1_name, match.team2_name, match.tournament_name, match.score)
    bot.send_message(user, message)


def message_future_match(team1: str, team2: str, tournament: str, date: datetime):
    return f'''
{team1} - {team2}
Турнир: {tournament}
Дата: {date} UTC
                '''


def message_result_match(team1: str, team2: str, tournament: str, score: str):
    return f'''
    {team1} - {team2}
    Турнир: {tournament}
    Результат: {score}
                    '''
