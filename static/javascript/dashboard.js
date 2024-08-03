const attendDay = document.getElementById('day');
const attendPercent = document.getElementById('percent');
const attendStart = document.getElementById('startday');

//학습률
//오늘치 학습을 모두 완료했는가?
document.addEventListener("DOMContentLoaded", async function () {
    const token = document.cookie;
    try{
        const response = await fetch("/api/user/me", {
            method: "GET",
            headers: {
                "Authorization": token,  // Bearer를 포함한 전체 토큰 값
            },
        });
        if (response.ok) {
            const data = await response.json();

            attendDay.innerHTML = `${data.attendance}일`;
            
        } else {
            console.error("Failed to fetch user info:", response.statusText);
        }
    } catch (error) {
    console.error("Error:", error);
}
});

//출석 부분
//1. 출석일수 2. 출석률 = 출석일/한달별날짜수 3. 가입날짜


//주제 그래프
//주제별로 얼만큼 완료했는지 막대그래프로 표시 (4개 주제)

