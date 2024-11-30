"""create user table

Revision ID: 57702fd2811c
Revises: 10296b58c8ff
Create Date: 2024-11-26 18:39:24.858536

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '57702fd2811c'
down_revision: Union[str, None] = '10296b58c8ff'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
