from sqlalchemy.orm import Session
from api.models import Ranking
from domain.ranking.ranking_schema import RankingCreate


def get_ranking_list(db: Session):
    return db.query(Ranking).all()


def get_ranking(db: Session, ranking_id: int):
    return db.query(Ranking).get(ranking_id)


def create_ranking(db: Session, ranking_create: RankingCreate):
    db_ranking = Ranking(
        user_id=ranking_create.user_id,
        tier=ranking_create.tier,
        point=ranking_create.point
    )
    db.add(db_ranking)
    db.commit()
    db.refresh(db_ranking)
    return db_ranking


def delete_ranking(db: Session, db_ranking: Ranking):
    db.delete(db_ranking)
    db.commit()
