import pytest

from src.extensions import session
from src.models import Users, Base, Teams


@pytest.fixture()
def start_db():
    Base.metadata.create_all()
    yield
    session.remove()
    Base.metadata.drop_all()


@pytest.fixture()
def add_start_user(start_db):
    test_user = Users(id=1)
    session.add(test_user)
    session.commit()


@pytest.fixture()
def add_start_team(start_db):
    test_team1 = Teams(id=1, name='NaVi', tag='NaVi')
    test_team2 = Teams(id=2, name='Virtus Pro', tag='VP')
    test_team3 = Teams(id=3, name='Team Spirit', tag='Spirit')
    test_team4 = Teams(id=4, name='Evil Genius', tag='EG')
    session.add(test_team1)
    session.add(test_team2)
    session.add(test_team3)
    session.add(test_team4)
    session.commit()


@pytest.fixture()
def add_teams_to_user(add_start_user, add_start_team):
    user = session.query(Users).first()
    teams = session.query(Teams).all()
    user.teams.append(teams[0])
    user.teams.append(teams[1])
    session.commit()
