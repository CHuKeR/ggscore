from datetime import datetime, timedelta

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from src.extensions import engine, session

Base = declarative_base(bind=engine)

association_table = Table('users_dota_teams', Base.metadata,
                          Column('bot_users_id', Integer, ForeignKey('bot_users.id')),
                          Column('dota_teams_id', Integer, ForeignKey('dota_teams.id'))
                          )


class Users(Base):
    __tablename__ = 'bot_users'
    id = Column(Integer, primary_key=True)
    teams = relationship(
        "Teams",
        secondary=association_table,
        back_populates="users")

    def get_user_teams(self):
        return [teams.tag for teams in self.teams]


class Teams(Base):
    __tablename__ = 'dota_teams'
    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    tag = Column(String(20))
    users = relationship(
        "Users",
        secondary=association_table,
        back_populates="teams")

    @classmethod
    def get_all_teams_tags(cls):
        teams_objects = session.query(cls).all()
        return [team.tag for team in teams_objects]


class Series(Base):
    __tablename__ = 'series'
    id = Column(Integer, primary_key=True)
    team1_name = Column(String(20))
    team2_name = Column(String(20))
    series_url = Column(String(256))
    score = Column(String(7), default='0:0')
    date = Column(DateTime)
    tournament_name = Column(String(256))
    finished = Column(Boolean)

    def get_series_score(self):
        pass

    def get_match_result_image(self, match: int):
        pass

    @classmethod
    def get_today_matches(cls):
        now_time = datetime.utcnow()
        end_period = (datetime.utcnow() + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        matches = session.query(cls).filter(cls.date > now_time).filter(cls.date < end_period).all()
        return matches

    @classmethod
    def get_finished_matches(cls):
        return session.query(cls).filter(cls.finished == True).all()

    @classmethod
    def delete_finished_matches(cls):
        session.query(cls).filter(cls.finished == True).delete(synchronize_session='fetch')
        session.commit()
