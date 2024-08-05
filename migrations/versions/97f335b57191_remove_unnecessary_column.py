"""remove unnecessary column

Revision ID: 97f335b57191
Revises: c2d561246fa8
Create Date: 2024-08-03 16:59:03.316816

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '97f335b57191'
down_revision: Union[str, None] = 'c2d561246fa8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
