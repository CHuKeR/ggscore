import pytest
from mock import patch
from src.worker import send_finished_matches_to_users, send_updated_matches_to_user
from src.worker import update_future_dota_matches, update_finished_dota_matches
from src.models import Series, Users
from src.extensions import session


@pytest.mark.worker
def test_update_future_matches_no_update(add_start_team, mock_dota_parser):
    update_future_dota_matches()
    assert session.query(Series).count() == 1


@pytest.mark.worker
def test_update_future_matches_with_update(start_matches, add_start_team, mock_dota_parser):
    updated_mathces = update_future_dota_matches()
    assert session.query(Series).count() == 2
    assert len(updated_mathces) == 1


@pytest.mark.worker
def test_update_future_matches_with_update(start_matches,
                                           add_start_team,
                                           add_teams_to_user,
                                           mock_telegram,
                                           mock_dota_parser,
                                           ):
    updated_matches = update_future_dota_matches()
    send_updated_matches_to_user(updated_matches)
    assert mock_telegram.call_count == 1


@pytest.mark.worker
def test_user_stop_bot(start_matches,
                       add_start_team,
                       add_teams_to_user,
                       mock_fail_telegram,
                       mock_dota_parser,
                       ):
    updated_matches = update_future_dota_matches()
    send_updated_matches_to_user(updated_matches)
    assert session.query(Users).count() == 0
