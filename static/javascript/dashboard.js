const attendDay = document.getElementById("day");
const attendPercent = document.getElementById("percent");
const attendStart = document.getElementById("startday");
const studyGraph = document.getElementById("studyGraph");
function getDaysInMonth(year, month) {
  return new Date(year, month, 0).getDate();
}

document.addEventListener("DOMContentLoaded", async function () {
  const token = document.cookie;
  let now = new Date();
  let year = now.getFullYear();
  let month = now.getMonth() + 1;

  let totalDays = getDaysInMonth(year, month);
  try {
    const response = await fetch("/api/user/me", {
      method: "GET",
      headers: {
        Authorization: token, // Bearer를 포함한 전체 토큰 값
      },
    });
    if (response.ok) {
      const data = await response.json();

      console.log(data);

      //학습률
      //오늘치 학습을 모두 완료했는가?

      let completedQuizzes = data.today_current_quiz.split(",").length;
      studyGraph.innerHTML = `${((completedQuizzes / 10) * 100).toFixed(1)}%`;

      //출석 부분
      //1. 출석일수 2. 출석률 = 출석일/한달별날짜수 3. 가입날짜
      attendDay.innerHTML = `${data.attendance}일`;

      attendPercent.innerHTML = `${(
        (data.attendance / totalDays) *
        100
      ).toFixed(1)}%`;

      attendStart.innerHTML = `${data.signupdate.slice(0, 10)}`;
    } else {
      console.error("Failed to fetch user info:", response.statusText);
    }
  } catch (error) {
    console.error("Error:", error);
  }
});

//주제 그래프
//주제별로 얼만큼 완료했는지 막대그래프로 표시 (4개 주제)
