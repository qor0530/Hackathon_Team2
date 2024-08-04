// 변수 설정
const tier = document.getElementById('tier');
const attendDay = document.getElementById('day');
const attendTime = document.getElementById('time');
const quizSum = document.getElementById('quiz');

const nickname = document.getElementsByClassName('userName');
const ranking = document.getElementsByClassName('rank');
const rankScore = document.getElementsByClassName('rankScore');

const subscribe = document.getElementById('subscribe');

function convertMinutesToHoursAndMinutes(totalMinutes) {
    const hours = Math.floor(totalMinutes / 60);
    const minutes = totalMinutes % 60;
    return { hours, minutes };
}

// DOMContentLoaded 이벤트 리스너
document.addEventListener("DOMContentLoaded", async function () {
    const token = document.cookie.split('; ').find(row => row.startsWith('access_token')).split('=')[1];
    try {
        const response = await fetch("/api/user/me", {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`,  // Bearer를 포함한 전체 토큰 값
            },
        });
        if (response.ok) {
            const data = await response.json();

            console.log(data);
            // username 설정
            nickname[0].innerHTML = data.nickname;
            // 학습 통계 설정
            let timeResult = convertMinutesToHoursAndMinutes(data.total_learning_time);
            attendTime.innerHTML = `${timeResult.hours}h ${timeResult.minutes}m`;
            attendDay.innerHTML = `${data.attendance}일`;

            if (data.subscription == false) {
                subscribe.innerHTML = `이용권 없음<br/><p>이용권 구매하기</p>`;
                subscribe.getElementsByTagName('p')[0].style.fontSize = '1.25rem';
                subscribe.getElementsByTagName('p')[0].style.fontFamily = 'Pretendard-Medium';
                subscribe.getElementsByTagName('p')[0].style.color = 'rgba(255,255,255,0.7)';
            }

            // 사용자의 티어와 랭킹을 가져오기 위해 API 호출
            const infoResponse = await fetch(`/api/ranking/user/${data.id}/info`, {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${token}`,
                },
            });

            if (infoResponse.ok) {
                const infoData = await infoResponse.json();

                const tierMap = {
                    iron: "iron.png",
                    bronze: "bronze.png",
                    silver: "silver.png",
                    gold: "gold.png",
                    platinum: "platinum.png",
                    emerald: "emerald.png",
                    diamond: "diamond.png",
                    master: "master.png"
                };

                const tierImage = tierMap[infoData.tier.toLowerCase()] || "empty.png";
                tier.src = `/static/images/${tierImage}`;
                ranking[0].innerHTML = `${infoData.tier} 리그`;
                rankScore[0].innerHTML = `${infoData.ranking_in_tier}`;
                
            } else {
                console.error("Failed to fetch user info:", infoResponse.statusText);
            }

            // 학습 통계 API 호출
            const statsResponse = await fetch(`/api/user/me/statistics`, {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${token}`,
                },
            });

            if (statsResponse.ok) {
                const statsData = await statsResponse.json();
                attendTime.innerHTML = `${convertMinutesToHoursAndMinutes(statsData.total_learning_time).hours}h ${convertMinutesToHoursAndMinutes(statsData.total_learning_time).minutes}m`;
                quizSum.innerHTML = `${statsData.quiz_solved}개`;
                attendDay.innerHTML = `${statsData.attendance_days}일`;
            } else {
                console.error("Failed to fetch statistics:", statsResponse.statusText);
            }

        } else {
            console.error("Failed to fetch user info:", response.statusText);
        }
    } catch (error) {
        console.error("Error:", error);
    }
});