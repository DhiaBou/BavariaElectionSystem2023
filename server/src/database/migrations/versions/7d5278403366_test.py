"""test

Revision ID: 7d5278403366
Revises: d0351cc56b45
Create Date: 2023-12-01 20:21:57.825314

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7d5278403366"
down_revision: Union[str, None] = "d0351cc56b45"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("erste_stimmzettel", sa.Column("StimmkreisId", sa.Integer(), nullable=True))
    op.create_foreign_key(None, "erste_stimmzettel", "stimmkreis", ["StimmkreisId"], ["StimmkreisId"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "erste_stimmzettel", type_="foreignkey")
    op.drop_column("erste_stimmzettel", "StimmkreisId")
    # ### end Alembic commands ###
