"""wahlergebnisse2018

Revision ID: 8e5d52cbaa5e
Revises: f8c8a33dedfe
Create Date: 2024-02-04 14:10:08.515330

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '8e5d52cbaa5e'
down_revision: Union[str, None] = 'f8c8a33dedfe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('wahlergebnisse2018',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('Partei', sa.String(length=255), nullable=True),
                    sa.Column('Erststimmen', sa.Integer(), nullable=True),
                    sa.Column('Zweitstimmen', sa.Integer(), nullable=True),
                    sa.Column('Gesamtstimmen', sa.Integer(), nullable=True),
                    sa.Column('SummeInProzent', sa.DECIMAL(precision=5, scale=2), nullable=True),
                    sa.Column('DifferenzZu2013', sa.DECIMAL(precision=5, scale=2), nullable=True),
                    sa.Column('SitzeGesamt', sa.Integer(), nullable=True),
                    sa.Column('DifferenzSitzeZu2013', sa.Integer(), nullable=True),
                    sa.Column('Direktmandate', sa.Integer(), nullable=True),
                    sa.Column('DifferenzDirektmandateZu2013', sa.Integer(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('wahlergebnisse2018')
    # ### end Alembic commands ###
