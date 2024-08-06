from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, Session
import random

# 데이터베이스 설정
DATABASE_URL = "sqlite:///./HACKATHON_TEAM2.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 데이터베이스 초기화 함수


def init_db():
    Base.metadata.create_all(bind=engine)

# Lecture 모델 정의


class Lecture(Base):
    __tablename__ = 'lectures'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    difficulty = Column(Integer, index=True)
    topic = Column(String, index=True)
    image = Column(String, index=True)
    description = Column(Text, index=True)

# WritingTask 모델 정의


class WritingTask(Base):
    __tablename__ = 'writing_tasks'

    id = Column(Integer, primary_key=True, index=True)
    lecture_id = Column(Integer, ForeignKey('lectures.id'), index=True)
    question = Column(Text, index=True)
    content = Column(Text, index=True)
    lecture = relationship('Lecture', back_populates='writing_tasks')


Lecture.writing_tasks = relationship(
    'WritingTask', order_by=WritingTask.id, back_populates='lecture')

# ComprehensionTask 모델 정의


class ComprehensionTask(Base):
    __tablename__ = 'comprehension_tasks'

    id = Column(Integer, primary_key=True, index=True)
    lecture_id = Column(Integer, ForeignKey('lectures.id'), index=True)
    question = Column(Text, index=True)
    content = Column(Text, index=True)
    conversation = Column(Text, index=True)
    options = Column(Text, index=True)
    answer = Column(String, index=True)
    lecture = relationship('Lecture', back_populates='comprehension_tasks')


Lecture.comprehension_tasks = relationship(
    'ComprehensionTask', order_by=ComprehensionTask.id, back_populates='lecture')

# 더미 데이터 추가 함수


def add_test_data():
    db: Session = SessionLocal()

    # Lecture 더미 데이터
    lecture_data = [
        {"title": "정치의 기초", "difficulty": 3, "topic": "정치 | 경제",
            "image": "images/economy.png", "description": "유럽 연합과 우크라이나의 현 상황"},
        {"title": "문학 101", "difficulty": 2, "topic": "문학",
            "image": "images/literature.png", "description": "한글의 역사와 세종대왕"},
        {"title": "기초 수학", "difficulty": 4, "topic": "수학 | 과학",
            "image": "images/math.png", "description": "수학에 대한 생각: 김민형 교수"},
        {"title": "과학 혁명", "difficulty": 5, "topic": "수학 | 과학",
            "image": "images/math.png", "description": "신 플라톤 주의에 대한 이해"},
        {"title": "시사 문제", "difficulty": 3, "topic": "시사",
            "image": "images/event.png", "description": "문대통령에게 아빠찬스?"},
        {"title": "고급 경제학", "difficulty": 4, "topic": "정치 | 경제",
            "image": "images/economy.png", "description": "에덤스미스의 국부론"},
        {"title": "현대 문학", "difficulty": 3, "topic": "문학",
            "image": "images/literature.png", "description": "어떤 나의 생각들은 세계가 된다."},
        {"title": "응용 수학", "difficulty": 5, "topic": "수학 | 과학",
            "image": "images/math.png", "description": "개똥철학 이해하기"},
        {"title": "기술 발전", "difficulty": 4, "topic": "수학 | 과학",
            "image": "images/math.png", "description": "피타고라스의 생애"},
        {"title": "국제 문제", "difficulty": 3, "topic": "시사",
            "image": "images/event.png", "description": "국력과 메달의 비례관계"},
        {"title": "정치의 심화", "difficulty": 4, "topic": "정치 | 경제",
            "image": "images/economy.png", "description": "정치의 심화 개념을 학습합니다."},
        {"title": "고전 문학", "difficulty": 3, "topic": "문학",
            "image": "images/literature.png", "description": "고전 문학 작품을 분석합니다."},
        {"title": "현대 사회 문제", "difficulty": 3, "topic": "시사",
            "image": "images/event.png", "description": "현대 사회 문제를 분석합니다."},
        {"title": "경제 정책", "difficulty": 4, "topic": "정치 | 경제",
            "image": "images/economy.png", "description": "경제 정책의 기초를 학습합니다."},
        {"title": "문학 이론", "difficulty": 3, "topic": "문학",
            "image": "images/literature.png", "description": "문학 이론을 학습합니다."},
        {"title": "사회학 개론", "difficulty": 4, "topic": "시사",
            "image": "images/event.png", "description": "사회학의 기초 개념을 학습합니다."},
    ]

    for data in lecture_data:
        existing_lecture = db.query(Lecture).filter(
            Lecture.title == data["title"]
        ).first()

        if not existing_lecture:
            new_lecture = Lecture(**data)
            db.add(new_lecture)

    db.commit()

    # WritingTask 더미 데이터
    writing_task_data = [
        {
            "lecture_id": 1,
            "question": "다음 글을 읽고, 문단의 핵심 내용을 담아 문장으로 요약하시오.",
            "content": "유럽연합(EU)이 우크라이나의 경제안정화와 재건을 돕기 위해 500억 유로(약 75조원) 규모의 금융지원을 개시했다. 이 중 1차분으로 42억 유로(약 6조원)이 승인되었으며, 지원금은 대출과 보조금 형태로 지급된다. 이번 지원은 우크라이나의 경제 재건, 연금 및 급여 지급, 공공서비스 제공 등을 돕기 위한 것이다. 우크라이나는 지원을 받기 위해 공공 재정 관리 개선 등의 경제 개혁을 이행해야 한다."
        },
        {
            "lecture_id": 2,
            "question": "다음 글을 읽고, 문단의 핵심 내용을 담아 문장으로 요약하시오.",
            "content": "세종대왕은 백성들이 한자를 이해하지 못해 불편해하는 것을 보고 훈민정음을 창제했다. 한글은 옥스퍼드대에서 세계 최고의 문자로 평가받았으며, 유네스코 연구에서도 최고의 문자로 선정되었다. 여러 학자와 작가들이 한글을 극찬하며, 세종대왕은 '언어와 언어학의 50대 주요 사상가'에 선정되었다. 유네스코는 문맹 퇴치의 공로로 '세종대왕 문맹 퇴치상'을 제정하여 한글의 우수성을 인정했다."
        },
        {
            "lecture_id": 3,
            "question": "다음 글을 읽고, 문단의 핵심 내용을 담아 문장으로 요약하시오.",
            "content": "김민형 워릭대 수학과 교수는 수학을 근본적으로 이해하려는 욕심이 수학을 어렵게 만든다고 말했다. 그는 바이올린의 음높이를 계산하는 공식을 예로 들어 수학의 실용성을 설명했다. 김 교수는 코로나19 확산 예측에도 수학이 활용될 수 있다고 했다. 표본을 통해 전체를 추정하는 포획-재포획 방법을 소개하며, 이는 코로나19 확산 예측에도 적용될 수 있다고 말했다. 그는 수학 대중교육의 중요성을 강조하며, 인공지능 시대에 수학 원리를 아는 것이 중요하다고 덧붙였다."
        },
        {
            "lecture_id": 4,
            "question": "다음 글을 읽고, 문단의 핵심 내용을 담아 문장으로 요약하시오.",
            "content": "르네상스는 고대 그리스와 로마 시대의 학문과 예술을 부흥시키려는 운동으로, 특히 신플라톤주의는 자연 세계를 수학으로 설명하려 했다. 신플라톤주의자들은 우주와 인간의 상호작용을 강조하며, 인간이 자연 현상에 영향을 미칠 수 있다고 믿었다. 이러한 사조는 코페르니쿠스의 태양중심설에 영향을 주었다. 종교 개혁 운동은 부패하지 않은 순수한 신앙으로 돌아가려 했으며, 가톨릭교회의 부패를 드러내고 새로운 과학의 가능성을 열었다."
        },
        {
            "lecture_id": 5,
            "question": "다음 글을 읽고, 문단의 핵심 내용을 담아 문장으로 요약하시오.",
            "content": "윤석열 대통령은 이숙연 신임 대법관 임명을 재가했다. 이숙연 대법관은 딸의 비상장 주식 거래로 '아빠 찬스' 논란이 있었으나, 논란에 대해 사과하고 37억원 상당의 주식을 기부한다고 밝혔다. 국회는 재석 271명 중 찬성 206명, 반대 58명, 기권 7명으로 임명동의안을 가결시켰다."
        },
        {
            "lecture_id": 6,
            "question": "다음 글을 읽고, 문단의 핵심 내용을 담아 문장으로 요약하시오.",
            "content": "아담 스미스는 경제학의 창시자로, 경제활동의 자유와 시장의 '보이지 않는 손'을 주장했다. 그는 국부론에서 분업의 중요성과 자본축적을 강조하며, 국가의 경제 통제를 비판했다. 스미스의 사상은 신흥 자본가 계급의 지지를 받았으나, 그의 자유방임 사상은 1980년대 신자유주의로 변질되었다. 스미스는 독점을 비판했고, 시장 기능이 잘 작동할 때의 한계를 인식했다. 오늘날 자유방임 대신 적절한 규제가 필요함을 강조했다."
        },
        {
            "lecture_id": 7,
            "question": "다음 글을 읽고, 문단의 핵심 내용을 담아 문장으로 요약하시오.",
            "content": "'개똥철학'은 진짜 학문이 아닌 세상과 인생을 보는 관점이나 고찰을 의미하며, 사회적 상식에서 벗어난 인생관을 가리킨다. 예로 라노벨 주인공의 철학이나 복잡한 철학적 단어들을 맥락 없이 사용하는 경우가 있다. 이는 이해 부족이나 설명 부족에서 비롯되며, 다른 사람의 생각을 이해하지 못하거나 마음에 들지 않을 때도 '개똥철학'이라 부르기도 한다."
        },
        {
            "lecture_id": 8,
            "question": "다음 글을 읽고, 문단의 핵심 내용을 담아 문장으로 요약하시오.",
            "content": "피타고라스(기원전 570년 ~ 기원전 495년)는 고대 그리스 철학자이자 피타고라스 학파의 창시자이다. 사모스 섬에서 태어나 여러 지방을 여행하며 학문을 쌓았고, 남부 이탈리아의 크로토네에서 종교적인 학파를 세웠다. 피타고라스는 철학과 종교 교리를 가르쳤으며, 특히 피타고라스의 정리로 잘 알려져 있다. 그러나 그의 공적 중 많은 부분이 그의 동료나 제자의 것일 가능성도 있다. 피타고라스는 모든 것이 수로 이루어져 있다고 믿었으며, 최초로 자신을 철학자라 부른 사람으로 알려져 있다."},
        {
            "lecture_id": 9,
            "question": "다음 글을 읽고, 문단의 핵심 내용을 담아 문장으로 요약하시오.",
            "content": "올림픽은 전 세계가 참여하는 큰 축제로, 경제력과 메달 성적이 밀접하게 연관되어 있다. 2012년 런던올림픽에서는 미국이 금메달 34개로 1위를 차지할 것으로 예상된다. 올림픽은 기업의 이미지와 선수의 명예를 높이는 기회이지만, 과도한 시설 투자로 경제성장에 부정적인 영향을 미칠 수도 있다. 경제적, 정치적 갈등을 잠시 잊고 모두가 하나 되는 축제로서 올림픽의 역할이 강조된다."
        },
        {
            "lecture_id": 10,
            "question": "다음 글을 읽고, 문단의 핵심 내용을 담아 문장으로 요약하시오.",
            "content": "한국 정부가 강제동원 피해자 배상 문제 해법으로 국내 재단을 통한 배상급 지급안을 발표하며, 일본의 반도체 핵심소재 3개 품목 수출규제에 대응한 세계무역기구(WTO) 분쟁해결 절차를 중단했다. 일본이 수출규제를 철회하지 않았음에도 우리 정부가 먼저 양보한 것은 굴복으로 보이며, 기업들의 국산화 투자에도 혼선이 예상된다. 일본과의 정책 대화에서 한국의 무역 관리 체계를 심사받게 된 것은 굴욕적이다. 정부는 소재·부품·장비 자립화 정책을 지속할 것이라 밝혔다."}
    ]

    for data in writing_task_data:
        existing_task = db.query(WritingTask).filter(
            WritingTask.lecture_id == data["lecture_id"],
            WritingTask.question == data["question"]
        ).first()

        if not existing_task:
            new_task = WritingTask(**data)
            db.add(new_task)

    db.commit()

    # ComprehensionTask 더미 데이터
    comprehension_task_data = [
        {
            "lecture_id": 11,
            "question": "다음 상황을 읽고, 두 사람의 대화의 이어질 내용으로 가장 적절한 것을 고르시오.",
            "content": "친구와 함께 학교 과제를 하던 중, 너와 친구는 서로 다른 의견을 가지고 논쟁이 일어났다. 너는 발표 자료에 그래프를 추가해야 한다고 생각하고, 친구는 텍스트만으로 충분하다고 주장한다.",
            "conversation": "나는 그래프를 추가하는 것이 좋다고 생각해. 시각적으로 정보를 전달하면 더 효과적일 것 같아. | 맞아, 하지만 우리에게는 시간도 부족하고 자료를 정리하는 데 많은 시간이 걸릴 거야.",
            "options": "1. 그래프는 불필요해. 그냥 텍스트만으로 하자.\n2. 그렇다면 그래프를 추가하지 말자. 시간은 부족하니까.\n3. 그건 맞아. 하지만 그래프가 자료의 핵심을 더 잘 전달할 수 있다면, 시간 투자할 가치가 있다고 봐.\n4. 그러면 텍스트도 없애고 그래프만 추가하자.\n5. 그래프도 텍스트도 다 필요 없어. 간단하게 하자.",
            "answer": 3
        },
        {
            "lecture_id": 12,
            "question": "다음 상황을 읽고, 두 사람의 대화의 이어질 내용으로 가장 적절한 것을 고르시오.",
            "content": "동료와 프로젝트 기한에 대해 이야기하고 있다. 너는 기한을 연장해야 한다고 생각하고, 동료는 현재 기한을 지켜야 한다고 주장한다.",
            "conversation": "나는 기한을 연장하는 것이 좋다고 생각해. 더 나은 결과를 얻기 위해서는 시간이 필요해. | 맞아, 하지만 우리는 이미 충분한 시간을 가졌고 이제는 결과를 제출해야 해.",
            "options": "1. 기한은 지켜야 해. 연장은 불필요해.\n2. 그렇다면 기한을 연장하지 말자. 시간이 부족해.\n3. 그건 맞아. 하지만 더 나은 결과를 위해 시간을 투자할 가치가 있어.\n4. 그러면 결과 제출을 포기하자.\n5. 기한도 결과도 다 필요 없어. 간단하게 하자.",
            "answer": 3
        },
        {
            "lecture_id": 13,
            "question": "다음 상황을 읽고, 두 사람의 대화의 이어질 내용으로 가장 적절한 것을 고르시오.",
            "content": "프로젝트 팀원들과 프로젝트 방향에 대해 논의하고 있다. 너는 새로운 접근 방식을 제안하고, 팀원은 기존 방식을 유지해야 한다고 주장한다.",
            "conversation": "나는 새로운 접근 방식을 시도하는 것이 좋다고 생각해. 더 창의적인 결과를 얻을 수 있을 것 같아. | 맞아, 하지만 기존 방식이 더 안정적이고 예측 가능한 결과를 줄 거야.",
            "options": "1. 새로운 접근 방식은 불필요해. 기존 방식만으로 충분해.\n2. 그렇다면 새로운 접근 방식을 시도하지 말자. 안정성이 중요해.\n3. 그건 맞아. 하지만 창의적인 결과를 위해 새로운 접근 방식을 시도할 가치가 있어.\n4. 그러면 기존 방식을 포기하고 새로운 접근 방식만 시도하자.\n5. 기존 방식도 새로운 접근 방식도 다 필요 없어. 간단하게 하자.",
            "answer": 3
        },
        {
            "lecture_id": 14,
            "question": "다음 상황을 읽고, 두 사람의 대화의 이어질 내용으로 가장 적절한 것을 고르시오.",
            "content": "동료와 회사의 새로운 정책에 대해 이야기하고 있다. 너는 새로운 정책이 필요하다고 생각하고, 동료는 기존 정책을 유지해야 한다고 주장한다.",
            "conversation": "나는 새로운 정책을 도입하는 것이 좋다고 생각해. 더 효율적인 결과를 얻을 수 있을 것 같아. | 맞아, 하지만 기존 정책이 더 안정적이고 예측 가능한 결과를 줄 거야.",
            "options": "1. 새로운 정책은 불필요해. 기존 정책만으로 충분해.\n2. 그렇다면 새로운 정책을 도입하지 말자. 안정성이 중요해.\n3. 그건 맞아. 하지만 효율적인 결과를 위해 새로운 정책을 도입할 가치가 있어.\n4. 그러면 기존 정책을 포기하고 새로운 정책만 도입하자.\n5. 기존 정책도 새로운 정책도 다 필요 없어. 간단하게 하자.",
            "answer": 3
        },
        {
            "lecture_id": 15,
            "question": "다음 상황을 읽고, 두 사람의 대화의 이어질 내용으로 가장 적절한 것을 고르시오.",
            "content": "친구와 주말 계획에 대해 이야기하고 있다. 너는 야외 활동을 제안하고, 친구는 실내 활동을 선호한다.",
            "conversation": "나는 야외 활동을 하는 것이 좋다고 생각해. 신선한 공기를 마시고 자연을 즐길 수 있을 것 같아. | 맞아, 하지만 실내 활동이 더 편안하고 안정적일 거야.",
            "options": "1. 야외 활동은 불필요해. 실내 활동만으로 충분해.\n2. 그렇다면 야외 활동을 하지 말자. 안정성이 중요해.\n3. 그건 맞아. 하지만 신선한 공기를 위해 야외 활동을 할 가치가 있어.\n4. 그러면 실내 활동을 포기하고 야외 활동만 하자.\n5. 야외 활동도 실내 활동도 다 필요 없어. 간단하게 하자.",
            "answer": 3
        },
        {
            "lecture_id": 16,
            "question": "다음 상황을 읽고, 두 사람의 대화의 이어질 내용으로 가장 적절한 것을 고르시오.",
            "content": "상사와 프로젝트 방향에 대해 이야기하고 있다. 너는 새로운 기술을 도입해야 한다고 생각하고, 상사는 기존 기술을 유지해야 한다고 주장한다.",
            "conversation": "나는 새로운 기술을 도입하는 것이 좋다고 생각해. 더 혁신적인 결과를 얻을 수 있을 것 같아. | 맞아, 하지만 기존 기술이 더 안정적이고 예측 가능한 결과를 줄 거야.",
            "options": "1. 새로운 기술은 불필요해. 기존 기술만으로 충분해.\n2. 그렇다면 새로운 기술을 도입하지 말자. 안정성이 중요해.\n3. 그건 맞아. 하지만 혁신적인 결과를 위해 새로운 기술을 도입할 가치가 있어.\n4. 그러면 기존 기술을 포기하고 새로운 기술만 도입하자.\n5. 기존 기술도 새로운 기술도 다 필요 없어. 간단하게 하자.",
            "answer": 3
        },
        {
            "lecture_id": 17,
            "question": "다음 상황을 읽고, 두 사람의 대화의 이어질 내용으로 가장 적절한 것을 고르시오.",
            "content": "친구와 여행 계획에 대해 이야기하고 있다. 너는 해외 여행을 제안하고, 친구는 국내 여행을 선호한다.",
            "conversation": "나는 해외 여행을 하는 것이 좋다고 생각해. 새로운 문화를 경험할 수 있을 것 같아. | 맞아, 하지만 국내 여행이 더 편안하고 안전할 거야.",
            "options": "1. 해외 여행은 불필요해. 국내 여행만으로 충분해.\n2. 그렇다면 해외 여행을 하지 말자. 안정성이 중요해.\n3. 그건 맞아. 하지만 새로운 문화를 경험하기 위해 해외 여행을 할 가치가 있어.\n4. 그러면 국내 여행을 포기하고 해외 여행만 하자.\n5. 해외 여행도 국내 여행도 다 필요 없어. 간단하게 하자.",
            "answer": 3
        },
        {
            "lecture_id": 18,
            "question": "다음 상황을 읽고, 두 사람의 대화의 이어질 내용으로 가장 적절한 것을 고르시오.",
            "content": "팀원과 프로젝트 방향에 대해 이야기하고 있다. 너는 새로운 도구를 사용해야 한다고 생각하고, 팀원은 기존 도구를 유지해야 한다고 주장한다.",
            "conversation": "나는 새로운 도구를 사용하는 것이 좋다고 생각해. 더 효율적인 결과를 얻을 수 있을 것 같아. | 맞아, 하지만 기존 도구가 더 안정적이고 예측 가능한 결과를 줄 거야.",
            "options": "1. 새로운 도구는 불필요해. 기존 도구만으로 충분해.\n2. 그렇다면 새로운 도구를 사용하지 말자. 안정성이 중요해.\n3. 그건 맞아. 하지만 효율적인 결과를 위해 새로운 도구를 사용할 가치가 있어.\n4. 그러면 기존 도구를 포기하고 새로운 도구만 사용하자.\n5. 기존 도구도 새로운 도구도 다 필요 없어. 간단하게 하자.",
            "answer": 3
        },
        {
            "lecture_id": 19,
            "question": "다음 상황을 읽고, 두 사람의 대화의 이어질 내용으로 가장 적절한 것을 고르시오.",
            "content": "동료와 프로젝트 일정에 대해 이야기하고 있다. 너는 일정을 연기해야 한다고 생각하고, 동료는 현재 일정을 유지해야 한다고 주장한다.",
            "conversation": "나는 일정을 연기하는 것이 좋다고 생각해. 더 나은 결과를 얻기 위해서는 시간이 필요해. | 맞아, 하지만 우리는 이미 충분한 시간을 가졌고 이제는 결과를 제출해야 해.",
            "options": "1. 일정은 지켜야 해. 연기는 불필요해.\n2. 그렇다면 일정을 연기하지 말자. 시간이 부족해.\n3. 그건 맞아. 하지만 더 나은 결과를 위해 시간을 투자할 가치가 있어.\n4. 그러면 결과 제출을 포기하자.\n5. 일정도 결과도 다 필요 없어. 간단하게 하자.",
            "answer": 3
        },
        {
            "lecture_id": 20,
            "question": "다음 상황을 읽고, 두 사람의 대화의 이어질 내용으로 가장 적절한 것을 고르시오.",
            "content": "친구와 식사 메뉴에 대해 이야기하고 있다. 너는 새로운 음식을 시도해야 한다고 생각하고, 친구는 익숙한 음식을 선호한다.",
            "conversation": "나는 새로운 음식을 시도하는 것이 좋다고 생각해. 새로운 맛을 경험할 수 있을 것 같아. | 맞아, 하지만 익숙한 음식이 더 안전하고 편안할 거야.",
            "options": "1. 새로운 음식은 불필요해. 익숙한 음식만으로 충분해.\n2. 그렇다면 새로운 음식을 시도하지 말자. 안전성이 중요해.\n3. 그건 맞아. 하지만 새로운 맛을 경험하기 위해 새로운 음식을 시도할 가치가 있어.\n4. 그러면 익숙한 음식을 포기하고 새로운 음식만 시도하자.\n5. 새로운 음식도 익숙한 음식도 다 필요 없어. 간단하게 하자.",
            "answer": 3
        }
    ]

    for data in comprehension_task_data:
        existing_task = db.query(ComprehensionTask).filter(
            ComprehensionTask.lecture_id == data["lecture_id"],
            ComprehensionTask.question == data["question"]
        ).first()

        if not existing_task:
            new_task = ComprehensionTask(**data)
            db.add(new_task)

    db.commit()
    db.close()


if __name__ == "__main__":
    init_db()
    add_test_data()
    print("Test data added")
