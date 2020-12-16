"""empty message

Revision ID: 99749dec1003
Revises: 5ba15e8df78c
Create Date: 2020-12-15 22:07:33.488615

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '99749dec1003'
down_revision = '5ba15e8df78c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('artist_show',
    sa.Column('artist_id', sa.Integer(), nullable=False),
    sa.Column('show_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['artist_id'], ['Artist.id'], ),
    sa.ForeignKeyConstraint(['show_id'], ['Show.id'], ),
    sa.PrimaryKeyConstraint('artist_id', 'show_id')
    )
    op.create_table('venue_show',
    sa.Column('venue_id', sa.Integer(), nullable=False),
    sa.Column('show_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['show_id'], ['Show.id'], ),
    sa.ForeignKeyConstraint(['venue_id'], ['Venue.id'], ),
    sa.PrimaryKeyConstraint('venue_id', 'show_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('venue_show')
    op.drop_table('artist_show')
    # ### end Alembic commands ###
