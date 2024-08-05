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
            "image": "lecture_image_1.jpg", "description": "정치의 기본 개념을 학습합니다."},
        {"title": "문학 101", "difficulty": 2, "topic": "문학",
            "image": "lecture_image_2.jpg", "description": "문학 분석의 기초를 학습합니다."},
        {"title": "기초 수학", "difficulty": 4, "topic": "수학 | 과학",
            "image": "lecture_image_3.jpg", "description": "수학의 기본 개념을 학습합니다."},
        {"title": "과학 혁명", "difficulty": 5, "topic": "수학 | 과학",
            "image": "lecture_image_4.jpg", "description": "과학 혁명의 주요 사건을 학습합니다."},
        {"title": "시사 문제", "difficulty": 3, "topic": "시사",
            "image": "lecture_image_5.jpg", "description": "현재 시사 문제를 분석합니다."},
        {"title": "고급 경제학", "difficulty": 4, "topic": "정치 | 경제",
            "image": "lecture_image_6.jpg", "description": "고급 경제 이론을 학습합니다."},
        {"title": "현대 문학", "difficulty": 3, "topic": "문학",
            "image": "lecture_image_7.jpg", "description": "현대 문학 작품을 분석합니다."},
        {"title": "응용 수학", "difficulty": 5, "topic": "수학 | 과학",
            "image": "lecture_image_8.jpg", "description": "수학적 원리의 응용을 학습합니다."},
        {"title": "기술 발전", "difficulty": 4, "topic": "수학 | 과학",
            "image": "lecture_image_9.jpg", "description": "최근 기술 발전을 학습합니다."},
        {"title": "국제 문제", "difficulty": 3, "topic": "시사",
            "image": "lecture_image_10.jpg", "description": "국제 시사 문제를 분석합니다."},
        {"title": "정치의 심화", "difficulty": 4, "topic": "정치 | 경제",
            "image": "lecture_image_11.jpg", "description": "정치의 심화 개념을 학습합니다."},
        {"title": "고전 문학", "difficulty": 3, "topic": "문학",
            "image": "lecture_image_12.jpg", "description": "고전 문학 작품을 분석합니다."},
        {"title": "현대 사회 문제", "difficulty": 3, "topic": "시사",
            "image": "lecture_image_15.jpg", "description": "현대 사회 문제를 분석합니다."},
        {"title": "경제 정책", "difficulty": 4, "topic": "정치 | 경제",
            "image": "lecture_image_16.jpg", "description": "경제 정책의 기초를 학습합니다."},
        {"title": "문학 이론", "difficulty": 3, "topic": "문학",
            "image": "lecture_image_17.jpg", "description": "문학 이론을 학습합니다."},
        {"title": "사회학 개론", "difficulty": 4, "topic": "시사",
            "image": "lecture_image_19.jpg", "description": "사회학의 기초 개념을 학습합니다."},
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
            "content": "기후 변화는 지구 생태계에 광범위한 영향을 미치고 있습니다. 평균 기온의 상승은 빙하와 극지방의 얼음을 녹이고, 이는 해수면 상승을 초래합니다. 이로 인해 해안가 지역과 저지대에 사는 사람들은 심각한 홍수와 침수 위험에 직면하게 됩니다. 또한, 기후 변화는 기상 패턴을 변화시켜 극단적인 날씨 현상의 빈도를 높이고 있습니다. 예를 들어, 폭염, 폭우, 가뭄, 허리케인 등과 같은 자연 재해의 발생 빈도와 강도가 증가하고 있습니다. 이러한 변화는 농업, 수자원 관리, 생물 다양성 등 여러 분야에 걸쳐 부정적인 영향을 미치며, 전 세계적으로 심각한 사회적, 경제적 문제를 야기합니다."
        },
        {
            "lecture_id": 2,
            "question": "다음 글을 읽고, 문단의 핵심 내용을 담아 문장으로 요약하시오.",
            "content": "문학 작품은 인간의 감정과 경험을 다루는 예술 형태입니다. 시, 소설, 희곡 등 다양한 형식을 통해 작가들은 자신의 생각과 감정을 표현하고 독자들과 소통합니다. 문학 작품을 읽음으로써 우리는 다양한 시대와 문화 속에서 살아가는 사람들의 삶을 이해할 수 있습니다."
        },
        {
            "lecture_id": 3,
            "question": "다음 글을 읽고, 문단의 핵심 내용을 담아 문장으로 요약하시오.",
            "content": "수학은 우리의 일상 생활과 밀접하게 연결되어 있습니다. 계산, 측정, 패턴 인식 등 수학적 원리는 여러 분야에서 활용됩니다. 수학을 공부함으로써 우리는 논리적 사고와 문제 해결 능력을 키울 수 있습니다."
        },
        {
            "lecture_id": 4,
            "question": "다음 글을 읽고, 문단의 핵심 내용을 담아 문장으로 요약하시오.",
            "content": "과학 혁명은 인류 역사에서 중요한 전환점을 의미합니다. 새로운 과학적 발견과 기술 혁신은 우리의 삶을 크게 변화시켰습니다. 과학 혁명은 우리가 세계를 이해하는 방식을 근본적으로 바꾸었고, 현대 과학의 기초를 다졌습니다."
        },
        {
            "lecture_id": 5,
            "question": "다음 글을 읽고, 문단의 핵심 내용을 담아 문장으로 요약하시오.",
            "content": "시사 문제는 우리 사회의 현재와 미래를 이해하는 데 중요한 역할을 합니다. 정치, 경제, 사회 등 다양한 분야의 이슈를 분석하고 이해함으로써 우리는 더 나은 결정을 내릴 수 있습니다."
        },
        {
            "lecture_id": 6,
            "question": "다음 글을 읽고, 문단의 핵심 내용을 담아 문장으로 요약하시오.",
            "content": "세계 경제는 복잡한 시스템으로, 다양한 요인들이 상호 작용하여 작동합니다. 경제 지표와 통계는 경제 상태를 파악하는 데 중요한 도구가 되며, 이를 통해 우리는 경제 정책을 수립하고 조정할 수 있습니다."
        },
        {
            "lecture_id": 7,
            "question": "다음 글을 읽고, 문단의 핵심 내용을 담아 문장으로 요약하시오.",
            "content": "현대 문학은 사회의 다양한 측면을 반영하며, 작가들은 이를 통해 독자들과 소통합니다. 문학 작품은 사회적 이슈를 제기하고, 독자들로 하여금 새로운 시각을 갖게 합니다."
        },
        {
            "lecture_id": 8,
            "question": "다음 글을 읽고, 문단의 핵심 내용을 담아 문장으로 요약하시오.",
            "content": "수학의 응용 분야는 매우 넓으며, 다양한 산업에서 중요한 역할을 합니다. 예를 들어, 엔지니어링, 경제학, 컴퓨터 과학 등 여러 분야에서 수학적 원리는 문제 해결과 혁신을 가능하게 합니다."
        },
        {
            "lecture_id": 9,
            "question": "다음 글을 읽고, 문단의 핵심 내용을 담아 문장으로 요약하시오.",
            "content": "과학 기술의 발전은 우리의 삶을 크게 변화시켰습니다. 새로운 기술들은 우리의 생활 방식을 혁신하고, 경제적 번영을 가져오는 동시에 새로운 도전 과제도 안겨줍니다."
        },
        {
            "lecture_id": 10,
            "question": "다음 글을 읽고, 문단의 핵심 내용을 담아 문장으로 요약하시오.",
            "content": "국제 시사 문제는 국가 간의 관계와 글로벌 이슈를 다룹니다. 이러한 문제들을 이해하는 것은 국제 사회에서의 효과적인 참여와 협력을 위해 필수적입니다."
        }
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
            "answer": str(random.randint(1, 5))
        },
        {
            "lecture_id": 12,
            "question": "다음 상황을 읽고, 두 사람의 대화의 이어질 내용으로 가장 적절한 것을 고르시오.",
            "content": "동료와 프로젝트 기한에 대해 이야기하고 있다. 너는 기한을 연장해야 한다고 생각하고, 동료는 현재 기한을 지켜야 한다고 주장한다.",
            "conversation": "나는 기한을 연장하는 것이 좋다고 생각해. 더 나은 결과를 얻기 위해서는 시간이 필요해. | 맞아, 하지만 우리는 이미 충분한 시간을 가졌고 이제는 결과를 제출해야 해.",
            "options": "1. 기한은 지켜야 해. 연장은 불필요해.\n2. 그렇다면 기한을 연장하지 말자. 시간이 부족해.\n3. 그건 맞아. 하지만 더 나은 결과를 위해 시간을 투자할 가치가 있어.\n4. 그러면 결과 제출을 포기하자.\n5. 기한도 결과도 다 필요 없어. 간단하게 하자.",
            "answer": str(random.randint(1, 5))
        },
        {
            "lecture_id": 13,
            "question": "다음 상황을 읽고, 두 사람의 대화의 이어질 내용으로 가장 적절한 것을 고르시오.",
            "content": "프로젝트 팀원들과 프로젝트 방향에 대해 논의하고 있다. 너는 새로운 접근 방식을 제안하고, 팀원은 기존 방식을 유지해야 한다고 주장한다.",
            "conversation": "나는 새로운 접근 방식을 시도하는 것이 좋다고 생각해. 더 창의적인 결과를 얻을 수 있을 것 같아. | 맞아, 하지만 기존 방식이 더 안정적이고 예측 가능한 결과를 줄 거야.",
            "options": "1. 새로운 접근 방식은 불필요해. 기존 방식만으로 충분해.\n2. 그렇다면 새로운 접근 방식을 시도하지 말자. 안정성이 중요해.\n3. 그건 맞아. 하지만 창의적인 결과를 위해 새로운 접근 방식을 시도할 가치가 있어.\n4. 그러면 기존 방식을 포기하고 새로운 접근 방식만 시도하자.\n5. 기존 방식도 새로운 접근 방식도 다 필요 없어. 간단하게 하자.",
            "answer": str(random.randint(1, 5))
        },
        {
            "lecture_id": 14,
            "question": "다음 상황을 읽고, 두 사람의 대화의 이어질 내용으로 가장 적절한 것을 고르시오.",
            "content": "동료와 회사의 새로운 정책에 대해 이야기하고 있다. 너는 새로운 정책이 필요하다고 생각하고, 동료는 기존 정책을 유지해야 한다고 주장한다.",
            "conversation": "나는 새로운 정책을 도입하는 것이 좋다고 생각해. 더 효율적인 결과를 얻을 수 있을 것 같아. | 맞아, 하지만 기존 정책이 더 안정적이고 예측 가능한 결과를 줄 거야.",
            "options": "1. 새로운 정책은 불필요해. 기존 정책만으로 충분해.\n2. 그렇다면 새로운 정책을 도입하지 말자. 안정성이 중요해.\n3. 그건 맞아. 하지만 효율적인 결과를 위해 새로운 정책을 도입할 가치가 있어.\n4. 그러면 기존 정책을 포기하고 새로운 정책만 도입하자.\n5. 기존 정책도 새로운 정책도 다 필요 없어. 간단하게 하자.",
            "answer": str(random.randint(1, 5))
        },
        {
            "lecture_id": 15,
            "question": "다음 상황을 읽고, 두 사람의 대화의 이어질 내용으로 가장 적절한 것을 고르시오.",
            "content": "친구와 주말 계획에 대해 이야기하고 있다. 너는 야외 활동을 제안하고, 친구는 실내 활동을 선호한다.",
            "conversation": "나는 야외 활동을 하는 것이 좋다고 생각해. 신선한 공기를 마시고 자연을 즐길 수 있을 것 같아. | 맞아, 하지만 실내 활동이 더 편안하고 안정적일 거야.",
            "options": "1. 야외 활동은 불필요해. 실내 활동만으로 충분해.\n2. 그렇다면 야외 활동을 하지 말자. 안정성이 중요해.\n3. 그건 맞아. 하지만 신선한 공기를 위해 야외 활동을 할 가치가 있어.\n4. 그러면 실내 활동을 포기하고 야외 활동만 하자.\n5. 야외 활동도 실내 활동도 다 필요 없어. 간단하게 하자.",
            "answer": str(random.randint(1, 5))
        },
        {
            "lecture_id": 16,
            "question": "다음 상황을 읽고, 두 사람의 대화의 이어질 내용으로 가장 적절한 것을 고르시오.",
            "content": "상사와 프로젝트 방향에 대해 이야기하고 있다. 너는 새로운 기술을 도입해야 한다고 생각하고, 상사는 기존 기술을 유지해야 한다고 주장한다.",
            "conversation": "나는 새로운 기술을 도입하는 것이 좋다고 생각해. 더 혁신적인 결과를 얻을 수 있을 것 같아. | 맞아, 하지만 기존 기술이 더 안정적이고 예측 가능한 결과를 줄 거야.",
            "options": "1. 새로운 기술은 불필요해. 기존 기술만으로 충분해.\n2. 그렇다면 새로운 기술을 도입하지 말자. 안정성이 중요해.\n3. 그건 맞아. 하지만 혁신적인 결과를 위해 새로운 기술을 도입할 가치가 있어.\n4. 그러면 기존 기술을 포기하고 새로운 기술만 도입하자.\n5. 기존 기술도 새로운 기술도 다 필요 없어. 간단하게 하자.",
            "answer": str(random.randint(1, 5))
        },
        {
            "lecture_id": 17,
            "question": "다음 상황을 읽고, 두 사람의 대화의 이어질 내용으로 가장 적절한 것을 고르시오.",
            "content": "친구와 여행 계획에 대해 이야기하고 있다. 너는 해외 여행을 제안하고, 친구는 국내 여행을 선호한다.",
            "conversation": "나는 해외 여행을 하는 것이 좋다고 생각해. 새로운 문화를 경험할 수 있을 것 같아. | 맞아, 하지만 국내 여행이 더 편안하고 안전할 거야.",
            "options": "1. 해외 여행은 불필요해. 국내 여행만으로 충분해.\n2. 그렇다면 해외 여행을 하지 말자. 안정성이 중요해.\n3. 그건 맞아. 하지만 새로운 문화를 경험하기 위해 해외 여행을 할 가치가 있어.\n4. 그러면 국내 여행을 포기하고 해외 여행만 하자.\n5. 해외 여행도 국내 여행도 다 필요 없어. 간단하게 하자.",
            "answer": str(random.randint(1, 5))
        },
        {
            "lecture_id": 18,
            "question": "다음 상황을 읽고, 두 사람의 대화의 이어질 내용으로 가장 적절한 것을 고르시오.",
            "content": "팀원과 프로젝트 방향에 대해 이야기하고 있다. 너는 새로운 도구를 사용해야 한다고 생각하고, 팀원은 기존 도구를 유지해야 한다고 주장한다.",
            "conversation": "나는 새로운 도구를 사용하는 것이 좋다고 생각해. 더 효율적인 결과를 얻을 수 있을 것 같아. | 맞아, 하지만 기존 도구가 더 안정적이고 예측 가능한 결과를 줄 거야.",
            "options": "1. 새로운 도구는 불필요해. 기존 도구만으로 충분해.\n2. 그렇다면 새로운 도구를 사용하지 말자. 안정성이 중요해.\n3. 그건 맞아. 하지만 효율적인 결과를 위해 새로운 도구를 사용할 가치가 있어.\n4. 그러면 기존 도구를 포기하고 새로운 도구만 사용하자.\n5. 기존 도구도 새로운 도구도 다 필요 없어. 간단하게 하자.",
            "answer": str(random.randint(1, 5))
        },
        {
            "lecture_id": 19,
            "question": "다음 상황을 읽고, 두 사람의 대화의 이어질 내용으로 가장 적절한 것을 고르시오.",
            "content": "동료와 프로젝트 일정에 대해 이야기하고 있다. 너는 일정을 연기해야 한다고 생각하고, 동료는 현재 일정을 유지해야 한다고 주장한다.",
            "conversation": "나는 일정을 연기하는 것이 좋다고 생각해. 더 나은 결과를 얻기 위해서는 시간이 필요해. | 맞아, 하지만 우리는 이미 충분한 시간을 가졌고 이제는 결과를 제출해야 해.",
            "options": "1. 일정은 지켜야 해. 연기는 불필요해.\n2. 그렇다면 일정을 연기하지 말자. 시간이 부족해.\n3. 그건 맞아. 하지만 더 나은 결과를 위해 시간을 투자할 가치가 있어.\n4. 그러면 결과 제출을 포기하자.\n5. 일정도 결과도 다 필요 없어. 간단하게 하자.",
            "answer": str(random.randint(1, 5))
        },
        {
            "lecture_id": 20,
            "question": "다음 상황을 읽고, 두 사람의 대화의 이어질 내용으로 가장 적절한 것을 고르시오.",
            "content": "친구와 식사 메뉴에 대해 이야기하고 있다. 너는 새로운 음식을 시도해야 한다고 생각하고, 친구는 익숙한 음식을 선호한다.",
            "conversation": "나는 새로운 음식을 시도하는 것이 좋다고 생각해. 새로운 맛을 경험할 수 있을 것 같아. | 맞아, 하지만 익숙한 음식이 더 안전하고 편안할 거야.",
            "options": "1. 새로운 음식은 불필요해. 익숙한 음식만으로 충분해.\n2. 그렇다면 새로운 음식을 시도하지 말자. 안전성이 중요해.\n3. 그건 맞아. 하지만 새로운 맛을 경험하기 위해 새로운 음식을 시도할 가치가 있어.\n4. 그러면 익숙한 음식을 포기하고 새로운 음식만 시도하자.\n5. 새로운 음식도 익숙한 음식도 다 필요 없어. 간단하게 하자.",
            "answer": str(random.randint(1, 5))
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
