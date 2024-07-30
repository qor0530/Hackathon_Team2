from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from config.database import get_db
from domain.ranking import ranking_crud, ranking_schema
from typing import List

router = APIRouter(
    prefix="/api/ranking",
)


@router.get("/list", response_model=List[ranking_schema.Ranking])
def ranking_list(db: Session = Depends(get_db)):
    return ranking_crud.get_ranking_list(db)


@router.get("/{ranking_id}", response_model=ranking_schema.Ranking)
def ranking_detail(ranking_id: int, db: Session = Depends(get_db)):
    ranking = ranking_crud.get_ranking(db, ranking_id)
    if not ranking:
        raise HTTPException(status_code=404, detail="Ranking not found")
    return ranking


@router.post("/", response_model=ranking_schema.Ranking, status_code=status.HTTP_201_CREATED)
def ranking_create(ranking_create: ranking_schema.RankingCreate, db: Session = Depends(get_db)):
    return ranking_crud.create_ranking(db, ranking_create)


@router.put("/{ranking_id}", response_model=ranking_schema.Ranking)
def ranking_update(ranking_id: int, ranking_update: ranking_schema.RankingUpdate, db: Session = Depends(get_db)):
    db_ranking = ranking_crud.get_ranking(db, ranking_id)
    if not db_ranking:
        raise HTTPException(status_code=404, detail="Ranking not found")
    return ranking_crud.update_ranking(db=db, db_ranking=db_ranking, ranking_update=ranking_update)


@router.delete("/{ranking_id}", status_code=status.HTTP_204_NO_CONTENT)
def ranking_delete(ranking_id: int, db: Session = Depends(get_db)):
    db_ranking = ranking_crud.get_ranking(db, ranking_id)
    if not db_ranking:
        raise HTTPException(status_code=404, detail="Ranking not found")
    ranking_crud.delete_ranking(db=db, db_ranking=db_ranking)
