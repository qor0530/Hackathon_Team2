from pydantic import BaseModel


class ComprehensionTaskBase(BaseModel):
    lecture_id: int
    question: str
    content: str
    conversation: str
    options: str  # JSON encoded list
    answer: str


class ComprehensionTaskCreate(ComprehensionTaskBase):
    pass


class ComprehensionTaskUpdate(ComprehensionTaskBase):
    pass


class ComprehensionTask(ComprehensionTaskBase):
    id: int

    class Config:
        orm_mode = True
