"""init

Revision ID: 4fb638246299
Revises: 
Create Date: 2020-05-28 20:09:47.251232

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4fb638246299'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bot_users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('dota_teams',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=20), nullable=True),
    sa.Column('tag', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('series',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('team1_name', sa.String(length=20), nullable=True),
    sa.Column('team2_name', sa.String(length=20), nullable=True),
    sa.Column('series_url', sa.String(length=256), nullable=True),
    sa.Column('score', sa.String(length=7), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('tournament_name', sa.String(length=256), nullable=True),
    sa.Column('finished', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users_dota_teams',
    sa.Column('bot_users_id', sa.Integer(), nullable=True),
    sa.Column('dota_teams_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['bot_users_id'], ['bot_users.id'], ),
    sa.ForeignKeyConstraint(['dota_teams_id'], ['dota_teams.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users_dota_teams')
    op.drop_table('series')
    op.drop_table('dota_teams')
    op.drop_table('bot_users')
    # ### end Alembic commands ###
