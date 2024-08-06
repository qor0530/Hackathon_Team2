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
            "level": 1,
            "subject": "정치 | 경제",
            "sentence": "이번 정책은 ____에 발표될 예정입니다.",
            "explanation": """지금 지나가고 있는 이날.""",
            "answer": "금일",
            "hint": "오늘.",
            "answer_explanation": "오늘은  오늘 다음 날입니다."
        },
        {
            "level": 3,
            "subject": "정치 | 경제",
            "sentence": "그는 정치적 문제에 대해 깊이 있는 ____를 펼쳤다.",
            "explanation": """어떤 문제에 대하여 서로 의견을 내어 토의함. 또는 그런 토의.""",
            "answer": "논의",
            "hint": "의논하다의 유식한 표현.",
            "answer_explanation": "논의는 어떤 문제에 대하여 서로 의견을 내어 토의하는 것입니다."
        },
        {
            "level": 2,
            "subject": "정치 | 경제",
            "sentence": "대통령은 이번 일에 ______ 사과를 전했습니다.",
            "explanation": """마음의 표현 정도가 매우 깊고 간절하다.""",
            "answer": "심심한",
            "hint": "아주 많이 소망한다.",
            "answer_explanation": "심심한은 마음의 표현 정도가 매우 깊고 간절하다는 의미입니다."
        },
        {
            "level": 5,
            "subject": "정치 | 경제",
            "sentence": "해외 현지 법인에 상당한 금액을 ____하다.",
            "explanation": """회사나 조합 따위 공공사업을 수행하기 위하여 구성원이 자본을 내는 일을 이른다.""",
            "answer": "출자",
            "hint": "자금을 내다.",
            "answer_explanation": "출자는 회사나 조합 따위 공공사업을 수행하기 위하여 구성원이 자본을 내는 일을 이르는 것을 나타냅니다."
        },
        {
            "level": 2,
            "subject": "정치 | 경제",
            "sentence": "회장은 이번 사건의 책임자를 모두 ____했다.",
            "explanation": """잘못을 저지른 사람에게 직무나 직업을 그만두게 하다.""",
            "answer": "파면",
            "hint": "자르다.",
            "answer_explanation": "파면은 잘못을 저지른 사람에게 직무나 직업을 그만두게 하는 것을 나타냅니다."
        },
        # 문학
        {
            "level": 2,
            "subject": "문학",
            "sentence": "이 시의 ____는 별입니다.",
            "explanation": """임시로 붙인 제목이다.""",
            "answer": "가제",
            "hint": "가짜",
            "answer_explanation": "가제는 임시로 붙인 제목을 나타냅니다."
        },
        {
            "level": 1,
            "subject": "문학",
            "sentence": "공부를 다 한 종화는 할 일이 없어 ____하다.",
            "explanation": """흥미 있는 일이 없어 지루하다.""",
            "answer": "무료",
            "hint": "심심하다.",
            "answer_explanation": "무료는 흥미 있는 일이 없어 지루하다는 의미를 나타냅니다."
        },
        {
            "level": 3,
            "subject": "문학",
            "sentence": "홍길동의 행방이 ____하다.",
            "explanation": """소식이나 행방 따위를 알 길이 없다.""",
            "answer": "묘연",
            "hint": "모른다.",
            "answer_explanation": "묘연은 소식이나 행방 따위를 알 길이 없다는 것을 나타냅니다."
        },
        {
            "level": 5,
            "subject": "문학",
            "sentence": "고길동은 성격이 ______하다.",
            "explanation": """성질이 외곬으로 곧아 융통성이 없다.""",
            "answer": "고지식",
            "hint": "사람이 꽉 막혔다.",
            "answer_explanation": "고지식은 성질이 외곬으로 곧아 융통성이 없다는 것을 나타냅니다."
        },
        {
            "level": 1,
            "subject": "문학",
            "sentence": "아기 돼지 삼형제는 ____한 가족이다.",
            "explanation": """한 가족의 생활이 원만하고 즐겁다.""",
            "answer": "단란",
            "hint": "사이가 좋다.",
            "answer_explanation": "단란은 한 가족의 생활이 원만하고 즐겁다는 것을 나타냅니다."
        },
        # 수학 | 과학
        {
            "level": 2,
            "subject": "수학 | 과학",
            "sentence": "피타고라스 정리는 ____ 그리스에 발견되었습니다.",
            "explanation": """역사 시대 구분의 하나.""",
            "answer": "고대",
            "hint": "옛날.",
            "answer_explanation": "고대는 역사 시대 구분의 하나입니다."
        },
        {
            "level": 1,
            "subject": "수학 | 과학",
            "sentence": "식을 계산해서 답을 ____하다.",
            "explanation": """판단이나 결론 따위를 이끌어 내다.""",
            "answer": "도출",
            "hint": "결과를 내다.",
            "answer_explanation": "도출은 판단이나 결론 따위를 이끌어 낸다는 의미를 나타냅니다."
        },
        {
            "level": 3,
            "subject": "수학 | 과학",
            "sentence": "______ 사고보다는 복합적 사고가 필요한 시대이다.",
            "explanation": """ 선처럼 길게 일렬로 나아가는. 또는 그런 것.""",
            "answer": "선형적",
            "hint": "하나의 선.",
            "answer_explanation": "선형적은  선처럼 길게 일렬로 나아가는 것을 나타냅니다."
        },
        {
            "level": 3,
            "subject": "수학 | 과학",
            "sentence": "희미한 형광등이 방 안을 ____하고 있다.",
            "explanation": """광선으로 밝게 비추다.""",
            "answer": "조명",
            "hint": "빛내다.",
            "answer_explanation": "조명은 광선으로 밝게 비추는 것을 나타냅니다."
        },
        {
            "level": 4,
            "subject": "수학 | 과학",
            "sentence": "핵 연구의 성공이 ____될 날을 손꼽아 기다리셨다.",
            "explanation": """꿈, 기대 따위가 실제로 이루어지다.""",
            "answer": "실현",
            "hint": "원하다.",
            "answer_explanation": "실현은 꿈, 기대 따위가 실제로 이루어지는 것을 나타냅니다."
        },
        # 시사
        {
            "level": 2,
            "subject": "시사",
            "sentence": "____한 줄도 모르고 일만 했다.",
            "explanation": """배가 고프다.""",
            "answer": "시장",
            "hint": "hungry.",
            "answer_explanation": "시장하다는 배가 고프다는 말을 나타냅니다."
        },
        {
            "level": 1,
            "subject": "시사",
            "sentence": "이번 발표는 ____ 에 이루어졌습니다.",
            "explanation": """발표가 이루어진 시점을 나타내는 말.
            특정 날짜를 기준으로 합니다.""",
            "answer": "오늘",
            "hint": "현재의 날짜.",
            "answer_explanation": "오늘은 현재의 날짜입니다."
        },
        {
            "level": 2,
            "subject": "시사",
            "sentence": "스포츠 센터를 착공 2년 만에 ____하였다.",
            "explanation": """공사를 다 마치다.""",
            "answer": "준공",
            "hint": "끝내다.",
            "answer_explanation": "준공은 공사를 다 마치는 것을 나타냅니다."
        },
        {
            "level": 1,
            "subject": "시사",
            "sentence": "운동선수는 ______이 좋다.",
            "explanation": """오랫동안 버티며 견디는 힘.""",
            "answer": "지구력",
            "hint": "끈기.",
            "answer_explanation": "지구력은 오랫동안 버티며 견디는 힘입니다."
        },
        {
            "level": 4,
            "subject": "시사",
            "sentence": "요즘은 옷차림에서 ________ 스타일이 유행한다.",
            "explanation": """의상이나 머리 모양 따위에서 남성과 여성의 구별이 없음.""",
            "answer": "유니섹스",
            "hint": "구별이 없다.",
            "answer_explanation": "유니섹스는 의상이나 머리 모양 따위에서 남성과 여성의 구별이 없음을 의미합니다."
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
