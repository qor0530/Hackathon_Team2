//변수설정
const attendDay = document.getElementById("day");
const attendPercent = document.getElementById("percent");
const attendStart = document.getElementById("startday");

const characterImg = document.getElementById('exp');

let studyGraph = document.getElementsByClassName('studyGraph');
const studyRateWrap = document.getElementById('studyRateWrap');
//함수
function getDaysInMonth(year, month) {
  return new Date(year, month, 0).getDate();
}

//api연결
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

      //exp이미지
      const expMap = {
        1: "level1.png",
        2: "level2.png",
        3: "level3.png",
        4: "level4.png",
        5: "level5.png"
      };

      const expImage = expMap[data.exp] || "empty.png";
      characterImg.src = `/static/images/level/${expImage}`;

      //학습률
      const statsResponse = await fetch(`/api/user/me/statistics`, {
        method: "GET",
        headers: {
            "Authorization": `Bearer ${token}`,
            },
        });

        //학습률 약간 정지
        if (statsResponse.ok) {
            const statsData = await statsResponse.json();
            console.log(statsData)
            quiz_data = (statsData.quiz_solved / 10) * 100;
            
            console.log(studyGraph);
        } else {
            console.error("Failed to fetch statistics:", statsResponse.statusText);
        }

      //출석 부분
      //1. 출석일수 2. 출석률 = 출석일/한달별날짜수 3. 가입날짜
      attendDay.innerHTML = `${data.attendance}일`;

      attendPercent.innerHTML = `${((data.attendance / totalDays) * 100).toFixed(1)}%`;

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

setTimeout(function start() {
  const bars = document.querySelectorAll('.bar');
  bars.forEach((bar, i) => {
      const countSpan = document.createElement('span');
      countSpan.classList.add('count');
      bar.appendChild(countSpan);
      setTimeout(() => {
          bar.style.width = bar.getAttribute('data-percent');
      }, i * 100);
  });
});
