"""empty message

Revision ID: fd555cac3a5e
Revises: 
Create Date: 2024-07-30 23:10:01.626971

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fd555cac3a5e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('lectures',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('difficulty', sa.Integer(), nullable=True),
    sa.Column('topic', sa.String(), nullable=True),
    sa.Column('image', sa.String(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_lectures_description'), 'lectures', ['description'], unique=False)
    op.create_index(op.f('ix_lectures_difficulty'), 'lectures', ['difficulty'], unique=False)
    op.create_index(op.f('ix_lectures_id'), 'lectures', ['id'], unique=False)
    op.create_index(op.f('ix_lectures_image'), 'lectures', ['image'], unique=False)
    op.create_index(op.f('ix_lectures_title'), 'lectures', ['title'], unique=False)
    op.create_index(op.f('ix_lectures_topic'), 'lectures', ['topic'], unique=False)
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
    op.create_table('tests',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_level', sa.Integer(), nullable=True),
    sa.Column('grow', sa.String(), nullable=True),
    sa.Column('purpose', sa.String(), nullable=True),
    sa.Column('theme', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tests_grow'), 'tests', ['grow'], unique=False)
    op.create_index(op.f('ix_tests_id'), 'tests', ['id'], unique=False)
    op.create_index(op.f('ix_tests_purpose'), 'tests', ['purpose'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('login_id', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('nickname', sa.String(), nullable=False),
    sa.Column('profile_image', sa.String(), nullable=True),
    sa.Column('learning_history', sa.Text(), nullable=True),
    sa.Column('total_learning_time', sa.Float(), nullable=True),
    sa.Column('level', sa.Integer(), nullable=True),
    sa.Column('ranking_score', sa.Float(), nullable=True),
    sa.Column('subscription', sa.Boolean(), nullable=True),
    sa.Column('ranking', sa.Integer(), nullable=True),
    sa.Column('attendance', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('login_id'),
    sa.UniqueConstraint('nickname')
    )
    op.create_table('comprehension_tasks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('lecture_id', sa.Integer(), nullable=True),
    sa.Column('question', sa.Text(), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('conversation', sa.Text(), nullable=True),
    sa.Column('options', sa.Text(), nullable=True),
    sa.Column('answer', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['lecture_id'], ['lectures.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_comprehension_tasks_answer'), 'comprehension_tasks', ['answer'], unique=False)
    op.create_index(op.f('ix_comprehension_tasks_content'), 'comprehension_tasks', ['content'], unique=False)
    op.create_index(op.f('ix_comprehension_tasks_conversation'), 'comprehension_tasks', ['conversation'], unique=False)
    op.create_index(op.f('ix_comprehension_tasks_id'), 'comprehension_tasks', ['id'], unique=False)
    op.create_index(op.f('ix_comprehension_tasks_lecture_id'), 'comprehension_tasks', ['lecture_id'], unique=False)
    op.create_index(op.f('ix_comprehension_tasks_options'), 'comprehension_tasks', ['options'], unique=False)
    op.create_index(op.f('ix_comprehension_tasks_question'), 'comprehension_tasks', ['question'], unique=False)
    op.create_table('rankings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('tier', sa.String(), nullable=False),
    sa.Column('point', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('writing_tasks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('lecture_id', sa.Integer(), nullable=True),
    sa.Column('question', sa.Text(), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['lecture_id'], ['lectures.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_writing_tasks_content'), 'writing_tasks', ['content'], unique=False)
    op.create_index(op.f('ix_writing_tasks_id'), 'writing_tasks', ['id'], unique=False)
    op.create_index(op.f('ix_writing_tasks_lecture_id'), 'writing_tasks', ['lecture_id'], unique=False)
    op.create_index(op.f('ix_writing_tasks_question'), 'writing_tasks', ['question'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_writing_tasks_question'), table_name='writing_tasks')
    op.drop_index(op.f('ix_writing_tasks_lecture_id'), table_name='writing_tasks')
    op.drop_index(op.f('ix_writing_tasks_id'), table_name='writing_tasks')
    op.drop_index(op.f('ix_writing_tasks_content'), table_name='writing_tasks')
    op.drop_table('writing_tasks')
    op.drop_table('rankings')
    op.drop_index(op.f('ix_comprehension_tasks_question'), table_name='comprehension_tasks')
    op.drop_index(op.f('ix_comprehension_tasks_options'), table_name='comprehension_tasks')
    op.drop_index(op.f('ix_comprehension_tasks_lecture_id'), table_name='comprehension_tasks')
    op.drop_index(op.f('ix_comprehension_tasks_id'), table_name='comprehension_tasks')
    op.drop_index(op.f('ix_comprehension_tasks_conversation'), table_name='comprehension_tasks')
    op.drop_index(op.f('ix_comprehension_tasks_content'), table_name='comprehension_tasks')
    op.drop_index(op.f('ix_comprehension_tasks_answer'), table_name='comprehension_tasks')
    op.drop_table('comprehension_tasks')
    op.drop_table('users')
    op.drop_index(op.f('ix_tests_purpose'), table_name='tests')
    op.drop_index(op.f('ix_tests_id'), table_name='tests')
    op.drop_index(op.f('ix_tests_grow'), table_name='tests')
    op.drop_table('tests')
    op.drop_index(op.f('ix_quizzes_subject'), table_name='quizzes')
    op.drop_index(op.f('ix_quizzes_sentence'), table_name='quizzes')
    op.drop_index(op.f('ix_quizzes_level'), table_name='quizzes')
    op.drop_index(op.f('ix_quizzes_id'), table_name='quizzes')
    op.drop_index(op.f('ix_quizzes_hint'), table_name='quizzes')
    op.drop_index(op.f('ix_quizzes_explanation'), table_name='quizzes')
    op.drop_index(op.f('ix_quizzes_answer_explanation'), table_name='quizzes')
    op.drop_index(op.f('ix_quizzes_answer'), table_name='quizzes')
    op.drop_table('quizzes')
    op.drop_index(op.f('ix_lectures_topic'), table_name='lectures')
    op.drop_index(op.f('ix_lectures_title'), table_name='lectures')
    op.drop_index(op.f('ix_lectures_image'), table_name='lectures')
    op.drop_index(op.f('ix_lectures_id'), table_name='lectures')
    op.drop_index(op.f('ix_lectures_difficulty'), table_name='lectures')
    op.drop_index(op.f('ix_lectures_description'), table_name='lectures')
    op.drop_table('lectures')
    # ### end Alembic commands ###