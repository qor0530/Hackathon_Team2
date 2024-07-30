"""empty message

Revision ID: fcda4ffab591
Revises: 
Create Date: 2024-07-27 15:21:37.619567

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fcda4ffab591'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('quizzes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('level', sa.Integer(), nullable=True),
    sa.Column('subject', sa.String(), nullable=True),
    sa.Column('sentence', sa.Text(), nullable=True),
    sa.Column('explanation', sa.Text(), nullable=True),
    sa.Column('answer', sa.String(), nullable=True),
    sa.Column('hint', sa.String(), nullable=True),
    sa.Column('answer_explanation', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_quizzes_answer'), 'quizzes', ['answer'], unique=False)
    op.create_index(op.f('ix_quizzes_answer_explanation'), 'quizzes', ['answer_explanation'], unique=False)
    op.create_index(op.f('ix_quizzes_explanation'), 'quizzes', ['explanation'], unique=False)
    op.create_index(op.f('ix_quizzes_hint'), 'quizzes', ['hint'], unique=False)
    op.create_index(op.f('ix_quizzes_id'), 'quizzes', ['id'], unique=False)
    op.create_index(op.f('ix_quizzes_level'), 'quizzes', ['level'], unique=False)
    op.create_index(op.f('ix_quizzes_sentence'), 'quizzes', ['sentence'], unique=False)
    op.create_index(op.f('ix_quizzes_subject'), 'quizzes', ['subject'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_quizzes_subject'), table_name='quizzes')
    op.drop_index(op.f('ix_quizzes_sentence'), table_name='quizzes')
    op.drop_index(op.f('ix_quizzes_level'), table_name='quizzes')
    op.drop_index(op.f('ix_quizzes_id'), table_name='quizzes')
    op.drop_index(op.f('ix_quizzes_hint'), table_name='quizzes')
    op.drop_index(op.f('ix_quizzes_explanation'), table_name='quizzes')
    op.drop_index(op.f('ix_quizzes_answer_explanation'), table_name='quizzes')
    op.drop_index(op.f('ix_quizzes_answer'), table_name='quizzes')
    op.drop_table('quizzes')
    # ### end Alembic commands ###