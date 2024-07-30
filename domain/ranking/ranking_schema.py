from pydantic import BaseModel
from typing import Optional


class RankingBase(BaseModel):
    bronze: Optional[int] = None
    silver: Optional[int] = None
    gold: Optional[int] = None
    platinum: Optional[int] = None
    emerald: Optional[int] = None
    diamond: Optional[int] = None
    master: Optional[int] = None


class RankingCreate(RankingBase):
    pass


class RankingUpdate(RankingBase):
    pass


class Ranking(RankingBase):
    id: int

    class Config:
        orm_mode = True
