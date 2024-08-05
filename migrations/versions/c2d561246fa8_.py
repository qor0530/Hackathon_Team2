"""empty message

Revision ID: c2d561246fa8
Revises: bfd988156b51
Create Date: 2024-08-03 16:39:48.047518

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c2d561246fa8'
down_revision: Union[str, None] = 'bfd988156b51'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # 백업 테이블 생성
    op.execute("ALTER TABLE rankings RENAME TO rankings_backup;")
    
    # 새로운 테이블 생성 (필요한 컬럼만 포함)
    op.create_table(
        'rankings',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer),
        sa.Column('score', sa.Integer),
        sa.Column('tier', sa.Enum('iron', 'bronze', 'silver', 'gold', 'platinum', 'emerald', 'diamond', 'master', name='tier'))
    )

    # 데이터 복사
    op.execute("""
        INSERT INTO rankings (id, user_id, score, tier)
        SELECT id, user_id, score, tier FROM rankings_backup;
    """)

    # 백업 테이블 삭제
    op.drop_table('rankings_backup')

def downgrade():
    # 백업 테이블 생성
    op.execute("ALTER TABLE rankings RENAME TO rankings_backup;")
    
    # 기존 테이블 생성
    op.create_table(
        'rankings',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer),
        sa.Column('score', sa.Integer),
        sa.Column('tier', sa.Enum('iron', 'bronze', 'silver', 'gold', 'platinum', 'emerald', 'diamond', 'master', name='tier')),
        sa.Column('point', sa.Integer)  # 예를 들어 point 컬럼이 제거되었을 경우
    )

    # 데이터 복사
    op.execute("""
        INSERT INTO rankings (id, user_id, score, tier)
        SELECT id, user_id, score, tier FROM rankings_backup;
    """)

    # 백업 테이블 삭제
    op.drop_table('rankings_backup')