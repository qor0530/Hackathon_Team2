from sqlalchemy.orm import Session
from api.models import Ranking
from domain.ranking.ranking_schema import RankingCreate, RankingUpdate


def get_ranking_list(db: Session):
    return db.query(Ranking).all()


def get_ranking(db: Session, ranking_id: int):
    return db.query(Ranking).get(ranking_id)


def create_ranking(db: Session, ranking_create: RankingCreate):
    db_ranking = Ranking(
        bronze=ranking_create.bronze,
        silver=ranking_create.silver,
        gold=ranking_create.gold,
        platinum=ranking_create.platinum,
        emerald=ranking_create.emerald,
        diamond=ranking_create.diamond,
        master=ranking_create.master
    )
    db.add(db_ranking)
    db.commit()
    db.refresh(db_ranking)
    return db_ranking


def update_ranking(db: Session, db_ranking: Ranking, ranking_update: RankingUpdate):
    db_ranking.bronze = ranking_update.bronze
    db_ranking.silver = ranking_update.silver
    db_ranking.gold = ranking_update.gold
    db_ranking.platinum = ranking_update.platinum
    db_ranking.emerald = ranking_update.emerald
    db_ranking.diamond = ranking_update.diamond
    db_ranking.master = ranking_update.master
    db.add(db_ranking)
    db.commit()
    db.refresh(db_ranking)
    return db_ranking


def delete_ranking(db: Session, db_ranking: Ranking):
    db.delete(db_ranking)
    db.commit()
