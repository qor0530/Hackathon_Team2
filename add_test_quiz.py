from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker, declarative_base, Session

# 데이터베이스 설정
DATABASE_URL = "sqlite:///./HACKATHON_TEAM2.db"  # 필요에 따라 변경
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 데이터베이스 초기화 함수


def init_db():
    Base.metadata.create_all(bind=engine)

# Quiz 모델 정의


class Quiz(Base):
    __tablename__ = 'quizzes'

    id = Column(Integer, primary_key=True, index=True)
    level = Column(Integer, index=True)
    subject = Column(String, index=True)
    sentence = Column(Text, index=True)
    explanation = Column(Text, index=True)
    answer = Column(String, index=True)
    hint = Column(String, index=True)
    answer_explanation = Column(Text, index=True)

# 더미 데이터 추가 함수


def add_test_data():
    db: Session = SessionLocal()

    quiz_data = [
        # 정치 | 경제
        {
            "level": 5,
            "subject": "정치 | 경제",
            "sentence": "이번 정책은 ____에 발표될 예정입니다.",
            "explanation": """발표 시점을 나타내는 말.
            특정 날짜 또는 시점을 기준으로 합니다.""",
            "answer": "내일",
            "hint": "오늘 다음 날.",
            "answer_explanation": "내일은 오늘 다음 날입니다."
        },
        {
            "level": 4,
            "subject": "정치 | 경제",
            "sentence": "경제 보고서는 ______에 제출됩니다.",
            "explanation": """제출 시점을 나타내는 말.
            일반적으로 마감일을 기준으로 합니다.""",
            "answer": "마감일",
            "hint": "제출 마지막 날.",
            "answer_explanation": "마감일은 제출의 마지막 날입니다."
        },
        {
            "level": 3,
            "subject": "정치 | 경제",
            "sentence": "새로운 세금 정책은 <span class='blank'></span>에 시행됩니다.",
            "explanation": """시행 시점을 나타내는 말.
            법안이 통과된 이후의 특정 시점을 나타냅니다.""",
            "answer": "다음 달",
            "hint": "이번 달 다음 달.",
            "answer_explanation": "다음 달은 이번 달 다음 달입니다."
        },
        {
            "level": 6,
            "subject": "정치 | 경제",
            "sentence": "회의는 <span class='blank'></span>에 시작됩니다.",
            "explanation": """회의 시작 시점을 나타내는 말.
            특정 시간을 기준으로 합니다.""",
            "answer": "오전 10시",
            "hint": "하루의 시작 시간 중 하나.",
            "answer_explanation": "오전 10시는 하루의 시작 시간 중 하나입니다."
        },
        {
            "level": 7,
            "subject": "정치 | 경제",
            "sentence": "예산안은 <span class='blank'></span>에 공개됩니다.",
            "explanation": """공개 시점을 나타내는 말.
            특정 날짜를 기준으로 합니다.""",
            "answer": "다음 주",
            "hint": "이번 주 다음 주.",
            "answer_explanation": "다음 주는 이번 주 다음 주입니다."
        },
        # 문학
        {
            "level": 2,
            "subject": "문학",
            "sentence": "이 시는 <span class='blank'></span>에 쓰여졌습니다.",
            "explanation": """작품이 쓰여진 시점을 나타내는 말.
            특정 연도를 기준으로 합니다.""",
            "answer": "1930년대",
            "hint": "1930년부터 1939년까지의 기간.",
            "answer_explanation": "1930년대는 1930년부터 1939년까지의 기간을 나타냅니다."
        },
        {
            "level": 1,
            "subject": "문학",
            "sentence": "이 소설은 <span class='blank'></span>에 출판되었습니다.",
            "explanation": """작품이 출판된 시점을 나타내는 말.
            특정 연도를 기준으로 합니다.""",
            "answer": "2000년",
            "hint": "새 천년이 시작된 해.",
            "answer_explanation": "2000년은 새 천년이 시작된 해입니다."
        },
        {
            "level": 3,
            "subject": "문학",
            "sentence": "작가는 <span class='blank'></span>에 이 소설을 완성했습니다.",
            "explanation": """작품이 완성된 시점을 나타내는 말.
            특정 연도를 기준으로 합니다.""",
            "answer": "1980년대",
            "hint": "1980년부터 1989년까지의 기간.",
            "answer_explanation": "1980년대는 1980년부터 1989년까지의 기간을 나타냅니다."
        },
        {
            "level": 5,
            "subject": "문학",
            "sentence": "이 책은 <span class='blank'></span>에 베스트셀러가 되었습니다.",
            "explanation": """베스트셀러가 된 시점을 나타내는 말.
            특정 연도를 기준으로 합니다.""",
            "answer": "1990년",
            "hint": "1990년대의 첫 해.",
            "answer_explanation": "1990년은 1990년대의 첫 해입니다."
        },
        {
            "level": 4,
            "subject": "문학",
            "sentence": "이 문학 작품은 <span class='blank'></span>에 발표되었습니다.",
            "explanation": """작품이 발표된 시점을 나타내는 말.
            특정 연도를 기준으로 합니다.""",
            "answer": "2010년",
            "hint": "2010년대의 첫 해.",
            "answer_explanation": "2010년은 2010년대의 첫 해입니다."
        },
        # 수학 | 과학
        {
            "level": 3,
            "subject": "수학 | 과학",
            "sentence": "피타고라스 정리는 <span class='blank'></span>에 발견되었습니다.",
            "explanation": """수학 이론이 발견된 시점을 나타내는 말.
            특정 시대를 기준으로 합니다.""",
            "answer": "고대 그리스",
            "hint": "기원전 5세기.",
            "answer_explanation": "고대 그리스는 기원전 5세기입니다."
        },
        {
            "level": 4,
            "subject": "수학 | 과학",
            "sentence": "상대성 이론은 <span class='blank'></span>에 발표되었습니다.",
            "explanation": """과학 이론이 발표된 시점을 나타내는 말.
            특정 연도를 기준으로 합니다.""",
            "answer": "1915년",
            "hint": "제1차 세계 대전 중.",
            "answer_explanation": "1915년은 제1차 세계 대전 중입니다."
        },
        {
            "level": 5,
            "subject": "수학 | 과학",
            "sentence": "DNA의 이중 나선 구조는 <span class='blank'></span>에 밝혀졌습니다.",
            "explanation": """과학 발견이 이루어진 시점을 나타내는 말.
            특정 연도를 기준으로 합니다.""",
            "answer": "1953년",
            "hint": "1950년대의 한 해.",
            "answer_explanation": "1953년은 1950년대의 한 해입니다."
        },
        {
            "level": 6,
            "subject": "수학 | 과학",
            "sentence": "양자 역학은 <span class='blank'></span>에 발전했습니다.",
            "explanation": """과학 분야가 발전한 시점을 나타내는 말.
            특정 시대를 기준으로 합니다.""",
            "answer": "20세기 초반",
            "hint": "1900년부터 1930년까지의 기간.",
            "answer_explanation": "20세기 초반은 1900년부터 1930년까지의 기간을 나타냅니다."
        },
        {
            "level": 7,
            "subject": "수학 | 과학",
            "sentence": "인공지능 연구는 <span class='blank'></span>에 급격히 발전했습니다.",
            "explanation": """과학 연구가 급격히 발전한 시점을 나타내는 말.
            특정 연도를 기준으로 합니다.""",
            "answer": "2010년대",
            "hint": "2010년부터 2019년까지의 기간.",
            "answer_explanation": "2010년대는 2010년부터 2019년까지의 기간을 나타냅니다."
        },
        # 시사
        {
            "level": 2,
            "subject": "시사",
            "sentence": "이번 사건은 <span class='blank'></span>에 발생했습니다.",
            "explanation": """사건이 발생한 시점을 나타내는 말.
            특정 날짜를 기준으로 합니다.""",
            "answer": "어제",
            "hint": "오늘의 전날.",
            "answer_explanation": "어제는 오늘의 전날입니다."
        },
        {
            "level": 1,
            "subject": "시사",
            "sentence": "이번 발표는 <span class='blank'></span>에 이루어졌습니다.",
            "explanation": """발표가 이루어진 시점을 나타내는 말.
            특정 날짜를 기준으로 합니다.""",
            "answer": "오늘",
            "hint": "현재의 날짜.",
            "answer_explanation": "오늘은 현재의 날짜입니다."
        },
        {
            "level": 3,
            "subject": "시사",
            "sentence": "회의는 <span class='blank'></span>에 종료되었습니다.",
            "explanation": """회의가 종료된 시점을 나타내는 말.
            특정 시간을 기준으로 합니다.""",
            "answer": "오후 5시",
            "hint": "하루의 끝을 향하는 시간 중 하나.",
            "answer_explanation": "오후 5시는 하루의 끝을 향하는 시간 중 하나입니다."
        },
        {
            "level": 4,
            "subject": "시사",
            "sentence": "새로운 법안은 <span class='blank'></span>에 통과되었습니다.",
            "explanation": """법안이 통과된 시점을 나타내는 말.
            특정 날짜를 기준으로 합니다.""",
            "answer": "지난주",
            "hint": "이번 주 이전의 주.",
            "answer_explanation": "지난주는 이번 주 이전의 주입니다."
        },
        {
            "level": 5,
            "subject": "시사",
            "sentence": "다음 회의는 <span class='blank'></span>에 열릴 예정입니다.",
            "explanation": """회의가 열릴 시점을 나타내는 말.
            특정 날짜를 기준으로 합니다.""",
            "answer": "다음 달",
            "hint": "이번 달 다음 달.",
            "answer_explanation": "다음 달은 이번 달 다음 달입니다."
        }
    ]

    for data in quiz_data:
        existing_quiz = db.query(Quiz).filter(
            Quiz.level == data["level"],
            Quiz.subject == data["subject"],
            Quiz.sentence == data["sentence"]
        ).first()

        if not existing_quiz:
            new_quiz = Quiz(**data)
            db.add(new_quiz)

    db.commit()
    db.close()


if __name__ == "__main__":
    init_db()
    add_test_data()
    print("Test data added")
