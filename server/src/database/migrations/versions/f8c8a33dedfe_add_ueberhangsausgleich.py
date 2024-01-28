"""add ueberhangsausgleich

Revision ID: f8c8a33dedfe
Revises: 3d7d5cd18aa5
Create Date: 2023-12-10 11:25:53.318201

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f8c8a33dedfe"
down_revision: Union[str, None] = "3d7d5cd18aa5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "ausgleichsmandate",
        sa.Column("Id", sa.Integer(), nullable=False),
        sa.Column("WahlkreisId", sa.Integer(), nullable=True),
        sa.Column("ParteiID", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["ParteiID"],
            ["parteien.ParteiID"],
        ),
        sa.ForeignKeyConstraint(
            ["WahlkreisId"],
            ["wahlkreis.WahlkreisId"],
        ),
        sa.PrimaryKeyConstraint("Id"),
    )
    op.create_table(
        "ueberhangsmandate",
        sa.Column("Id", sa.Integer(), nullable=False),
        sa.Column("WahlkreisId", sa.Integer(), nullable=True),
        sa.Column("ParteiID", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["ParteiID"],
            ["parteien.ParteiID"],
        ),
        sa.ForeignKeyConstraint(
            ["WahlkreisId"],
            ["wahlkreis.WahlkreisId"],
        ),
        sa.PrimaryKeyConstraint("Id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("ueberhangsmandate")
    op.drop_table("ausgleichsmandate")
    # ### end Alembic commands ###
