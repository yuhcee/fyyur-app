"""empty message

Revision ID: e20d13014c30
Revises: 7d5e3deea753
Create Date: 2022-07-22 12:20:10.689454

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e20d13014c30'
down_revision = '7d5e3deea753'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artists', sa.Column('website', sa.String(length=120), nullable=True))
    op.add_column('artists', sa.Column('seeking_description', sa.String(length=120), nullable=True))
    op.add_column('artists', sa.Column('seeking_venue', sa.Boolean(), nullable=True))
    op.add_column('venues', sa.Column('genres', sa.String(length=120), nullable=True))
    op.add_column('venues', sa.Column('website', sa.String(length=120), nullable=True))
    op.add_column('venues', sa.Column('seeking_description', sa.String(length=120), nullable=True))
    op.add_column('venues', sa.Column('seeking_talent', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('venues', 'seeking_talent')
    op.drop_column('venues', 'seeking_description')
    op.drop_column('venues', 'website')
    op.drop_column('venues', 'genres')
    op.drop_column('artists', 'seeking_venue')
    op.drop_column('artists', 'seeking_description')
    op.drop_column('artists', 'website')
    # ### end Alembic commands ###
