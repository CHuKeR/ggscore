import pytest

from src.bot.services import add_user, get_settings_keyboard,     get_add_teams_keyboard

from src.extensions import session
from src.models import Users


@pytest.mark.user
def test_add_user(start_db):
    add_user(1)
    users_count = session.query(Users).count()
    assert users_count == 1


@pytest.mark.keyboard
def test_setting_keyboard():
    keyboard = get_settings_keyboard()
    assert len(keyboard.keyboard) == 2


@pytest.mark.keyboard
def test_add_teams_keyboard(add_teams_to_user):
    keyboard = get_add_teams_keyboard('add_teams_0', 1)
