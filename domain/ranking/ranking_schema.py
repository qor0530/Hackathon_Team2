from pydantic import BaseModel


class RankingBase(BaseModel):
    user_id: int
    tier: str
    score: float


class RankingCreate(RankingBase):
    pass


class RankingUpdate(RankingBase):
    pass


class Ranking(RankingBase):
    id: int

    class Config:
        orm_mode = True
