import pytest

from src.bot.services import add_user, get_settings_keyboard, get_add_teams_keyboard, add_team, delete_team

from src.extensions import session
from src.models import Users


@pytest.mark.user
def test_start(start_db):
    add_user(1)
    users_count = session.query(Users).count()
    assert users_count == 1


@pytest.mark.keyboard
def test_setting():
    keyboard = get_settings_keyboard()
    assert len(keyboard.keyboard) == 2


@pytest.mark.keyboard
def test_add_teams_keyboard(add_teams_to_user):
    keyboard = get_add_teams_keyboard('add_teams_0', 1)
    assert len(keyboard.keyboard) == 3


@pytest.mark.bot
def test_delete_teams_keyboard(add_teams_to_user):
    keyboard = get_add_teams_keyboard('delete_teams_0', 1)
    assert len(keyboard.keyboard) == 3


@pytest.mark.bot
def test_add_teams_to_user(add_teams_to_user):
    add_team('add_3', 1)
    keyboard = get_add_teams_keyboard('add_teams_0', 1)
    assert len(keyboard.keyboard) == 2


@pytest.mark.bot
def test_add_teams_to_user(add_teams_to_user):
    delete_team('delete_1', 1)
    keyboard = get_add_teams_keyboard('add_teams_0', 1)
    assert len(keyboard.keyboard) == 4
