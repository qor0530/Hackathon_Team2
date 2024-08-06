// 페이지를 전환하는 함수
function showPage(pageId) {
    var pages = document.querySelectorAll('.page');
    pages.forEach(function(page) {
        page.classList.remove('active');
    });
    document.getElementById(pageId).classList.add('active');
}

// '다음' 버튼 클릭 시 호출되는 함수
function nextPage(pageId) {
    showPage(pageId);
}

// '이전' 버튼 클릭 시 호출되는 함수
function prevPage(pageId) {
    showPage(pageId);
}

// 문서가 로드된 후 '학습하러 가기' 버튼 클릭 이벤트 추가
document.addEventListener('DOMContentLoaded', function() {
    var learnButton = document.getElementById('learnButton');
    if (learnButton) {
        learnButton.addEventListener('click', function() {
            window.location.href = '/dashboard'; // 실제 대시보드 HTML 파일 경로
        });
    } else {
        console.error('학습하러 가기 버튼을 찾을 수 없습니다.');
    }
});
