from src.bot.messages import send_future_match, send_result_match
from src.extensions import session
from src.logger import create_logger
from src.models import Series
from src.models import Teams
from src.models import Users
from src.parser.dota_series import DotaParser

logger = create_logger()


def send_future_matches_to_users():
    users = session.query(Users).all()
    for user in users:
        user_teams = user.get_user_teams()
        matches = Series.get_today_matches()
        for match in matches:
            if match.team1_name in user_teams or match.team2_name in user_teams:
                send_future_match(user.id, match)


def send_updated_matches_to_user(matches: list):
    users_for_update = get_users_to_updates(matches)
    for user in users_for_update:
        user_teams = user.get_user_teams()
        for match in matches:
            if match.team1_name in user_teams or match.team2_name in user_teams:
                send_future_match(user, match)


def get_users_to_updates(matches: list):
    teams_list = set([match.team1_name for match in matches] + [match.team2_name for match in matches])
    teams_object = session.query(Teams.id).filter(Teams.tag.in_(teams_list))
    users_for_update = session.query(Users).filter(Users.teams.any(Teams.id.in_(teams_object))).all()
    return users_for_update


def send_finished_matches_to_users():
    users = session.query(Users).all()
    for user in users:
        user_teams = user.get_user_teams()
        matches = Series.get_finished_matches()
        for match in matches:
            if match.team1_name in user_teams or match.team2_name in user_teams:
                send_result_match(user.id, match)
    Series.delete_finished_matches()


def update_future_dota_matches():
    updated_matches = []
    dota_parser = DotaParser()
    logger.info('Start updating future matches')
    matches = dota_parser.parse_future_matches()
    teams = Teams.get_all_teams_tags()
    for match in matches:
        updated = False
        if match['team1_name'] in teams or match['team2_name'] in teams:
            seria = session.query(Series).filter(Series.id == match['seria_id']).first()
            if seria is None:
                seria = Series(id=match['seria_id'],
                               team1_name=match['team1_name'],
                               team2_name=match['team2_name'],
                               tournament_name=match['tour_title'],
                               series_url=match['match_link'],
                               date=match['date'],
                               finished=False)

                session.add(seria)
            else:
                if match['date'] is not None and seria.date != match['date']:
                    seria.date = match['date']
                    updated = True
                if match['team1_name'] != seria.team1_name:
                    seria.team1_name = match['team1_name']
                    updated = True
                if match['team2_name'] != seria.team2_name:
                    seria.team2_name = match['team2_name']
                    updated = True
            if updated:
                updated_matches.append(seria)
            try:
                session.commit()
            except Exception as exc:
                logger.error(exc)
                session.rollback()
    return updated_matches


def update_finished_dota_matches():
    dota_parser = DotaParser()
    logger.info('Start update finished matches')
    matches = dota_parser.parse_finished_matches()
    for match in matches:
        seria = session.query(Series).filter(Series.id == match['seria_id']).first()
        if seria is not None:
            seria.score = match['score']
            seria.finished = True
        else:
            logger.error(f'Match with {match["seria_id"]} not in database!')
        try:
            session.commit()
        except Exception as exc:
            logger.error(exc)
            session.rollback()
