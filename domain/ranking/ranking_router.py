from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from config.database import SessionLocal
from domain.ranking.ranking_crud import get_rankings, update_user_score, get_users_by_tier, get_user_tier_by_user_id
from api.models import Tier, Ranking
from domain.user import user_crud, user_schema
SECRET_KEY = "0db75ab2ce9e9f2ebe7f231f01fdcb11bd94219f5c71194b537c70bf6d80a8f3"
ALGORITHM = "HS256"

router = APIRouter(prefix="/api/ranking")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def read_rankings(db: Session = Depends(get_db)):
    return get_rankings(db)

@router.put("/{user_id}/score")
def update_score(user_id: int, score: int, db: Session = Depends(get_db)):
    user = update_user_score(db, user_id, score)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/tier/{tier}")
def read_users_by_tier(tier: Tier, db: Session = Depends(get_db)):
    users = get_users_by_tier(db, tier)
    if not users:
        raise HTTPException(status_code=404, detail="No users found in this tier")
    return users

@router.get("/me/tier")
def read_my_tier(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization cookie missing",
        )

    token = token.replace("Bearer ", "")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        login_id: str = payload.get("sub")
        if login_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    user = user_crud.get_user_login_id(db, login_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    tier = get_user_tier_by_user_id(db, user.id)
    if not tier:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User tier not found")

    return {"tier": tier}

@router.get("/{user_id}/nickname")
def read_user_nickname(user_id: int, db: Session = Depends(get_db)):
    user = user_crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"nickname": user.nickname}

@router.get("/{user_id}/score")
def read_user_score(user_id: int, db: Session = Depends(get_db)):
    user = db.query(Ranking).filter(Ranking.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"score": user.score}

@router.get("/{user_id}/ranking")
def read_user_ranking(user_id: int, db: Session = Depends(get_db)):
    users = db.query(Ranking).order_by(Ranking.score.desc()).all()
    user_rank = next((i for i, user in enumerate(users, 1) if user.user_id == user_id), None)
    if user_rank is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"ranking": user_rank}

@router.get("/user/{user_id}/info")
def read_user_info(user_id: int, db: Session = Depends(get_db)):
    # 특정 사용자의 정보 가져오기
    user = db.query(Ranking).filter(Ranking.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # 해당 티어의 사용자들을 점수 순으로 정렬
    users_in_tier = db.query(Ranking).filter(Ranking.tier == user.tier).order_by(Ranking.score.desc()).all()
    # 특정 사용자의 티어 내 랭킹 찾기
    user_rank_in_tier = next((i for i, u in enumerate(users_in_tier, 1) if u.user_id == user_id), None)

    return {
        "tier": user.tier.name,  # Enum의 이름을 반환
        "ranking_in_tier": user_rank_in_tier
    }
