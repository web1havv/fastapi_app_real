"""add user table

Revision ID: 2a7f45686890
Revises: 2fe029f628a9
Create Date: 2025-01-07 17:44:04.856144

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2a7f45686890'
down_revision: Union[str, None] = '2fe029f628a9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


