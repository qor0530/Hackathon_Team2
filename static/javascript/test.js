let tests = [
    ` <div class="container">
    <div class="sidebar">
        <div class="character">
            캐릭터<br>(일러스트)
        </div>
    </div>
    <div class="main-content">
        <div class="progress-bar">
            <div class="progress"></div>
        </div>
        <div class="question">
            <span class="highlight">'더 리더'</span>를 통해 무엇을 기르고 싶나요?
        </div>
        <div class="options">
            <div class="option"></div>
            <div class="option"></div>
            <div class="option"></div>
            <div class="option"></div>
            <div class="option"></div>
            <div class="option selected"></div>
            <div class="option"></div>
        </div>
        <button class="next-button">다음</button>
    </div>
    </div>`,

    `    <div class="container">
    <div class="sidebar">
        <div class="character">
            캐릭터<br>(일러스트)
        </div>
    </div>
    <div class="main-content">
        <div class="progress-bar">
            <div class="progress"></div>
        </div>
        <div class="question">
            어느 <span class="highlight">목적</span>으로 읽기 실력을 향상하고 싶으신가요?
        </div>
        <div class="options">
            <div class="option"></div>
            <div class="option"></div>
            <div class="option selected"></div>
            <div class="option"></div>
            <div class="option"></div>
            <div class="option"></div>
        </div>
        <div class="buttons">
            <button class="prev-button">이전</button>
            <button class="next-button">다음</button>
        </div>
    </div>
    </div>`,

    `    <div class="container">
    <div class="sidebar">
        <div class="character">
            캐릭터<br>(일러스트)
        </div>
    </div>
    <div class="main-content">
        <div class="progress-bar">
            <div class="progress"></div>
        </div>
        <div class="question">
            <span class="highlight">관심 있는 주제</span>를 모두 선택해주세요!
        </div>
        <div class="options">
            <div class="option selected"></div>
            <div class="option"></div>
            <div class="option"></div>
            <div class="option selected"></div>
        </div>
        <div class="buttons">
            <button class="prev-button">이전</button>
            <button class="next-button">다음</button>
        </div>
    </div>
    </div>`,

    `    <div class="container">
    <div class="sidebar">
        <div class="character">
            캐릭터<br>(일러스트)
        </div>
    </div>
    <div class="main-content">
        <div class="progress-bar">
            <div class="progress"></div>
        </div>
        <div class="question">
            내 <span class="highlight">현재 읽기 실력</span>은 어디에 가까운가요?
        </div>
        <div class="options">
            <div class="option"></div>
            <div class="option selected"></div>
            <div class="option"></div>
        </div>
        <div class="buttons">
            <button class="prev-button">이전</button>
            <button class="next-button">다음</button>
        </div>
    </div>
    </div>`,

    `    <div class="container">
    <div class="sidebar">
        <div class="character">
            캐릭터<br>(일러스트)
        </div>
    </div>
    <div class="main-content">
        <div class="progress-bar">
            <div class="progress"></div>
        </div>
        <div class="question">
            주어진 상황에 알맞는 단어를 선택해주세요.
        </div>
        <div class="buttons">
            <button class="prev-button">이전</button>
            <button class="next-button">다음</button>
        </div>
    </div>
    </div>`,

    `    <div class="container">
    <div class="sidebar">
        <div class="character">
            캐릭터<br>(일러스트)
        </div>
    </div>
    <div class="main-content">
        <div class="progress-bar">
            <div class="progress"></div>
        </div>
        <div class="question">
            이 뜻에 해당하는 단어를 선택해주세요.
        </div>
        <div class="buttons">
            <button class="prev-button">이전</button>
            <button class="next-button">다음</button>
        </div>
    </div>
    </div>`,

    `    <div class="container">
    <div class="sidebar">
        <div class="character">
            캐릭터<br>(일러스트)
        </div>
    </div>
    <div class="main-content">
        <div class="progress-bar">
            <div class="progress"></div>
        </div>
        <div class="question">
            ‘ㅇㅇ'과 의미가 가장 비슷한 말을 선택해주세요.
        </div>
        <div class="buttons">
            <button class="prev-button">이전</button>
            <button class="next-button">다음</button>
        </div>
    </div>
    </div>`,

    `    <div class="container">
    <div class="sidebar">
        <div class="character">
            캐릭터<br>(일러스트)
        </div>
    </div>
    <div class="main-content">
        <div class="progress-bar">
            <div class="progress"></div>
        </div>
        <div class="question">
            내 <span class="highlight">현재 읽기 실력</span>은 어디에 가까운가요?
        </div>
        <div class="buttons">
            <button class="prev-button">이전</button>
            <button class="next-button">다음</button>
        </div>
    </div>
    </div>`,

    `    <div class="container">
    <div class="center-panel">
        <div class="header">
            감사합니다!
        </div>
        <div class="character">
            캐릭터<br>(일러스트)
        </div>
        <button class="next-button">학습하러 가기</button>
    </div>
    </div>`
];

let currentIndex = 0;

function getNextTest() {
    if (currentIndex < tests.length) {
        let currentTest = tests[currentIndex];
        currentIndex++;
        return currentTest;
    } else {
        return "<div>모든 테스트를 완료했습니다.</div>";
    }
}

function setupButtonListener() {
    const nextButton = document.querySelector('.next-button');
    if (nextButton) {
        nextButton.addEventListener('click', () => {
            let nextTest = getNextTest();
            document.body.innerHTML = nextTest;
            setupButtonListener(); // 새로운 페이지에서 다시 버튼 리스너 설정
        });
    }
}

// 초기 리스너 설정
setupButtonListener();