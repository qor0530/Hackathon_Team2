//변수설정
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

            console.log(data)
            //username 설정
            nickname[0].innerHTML = data.nickname;
            //ranking 설정  
            rankScore[0].innerHTML = data.ranking;

            //학습통계
            //1. 학습 시간 2. 푼 퀴즈 수 3. 누적 출석일수
            let timeResult = convertMinutesToHoursAndMinutes(data.total_learning_time);
            attendTime.innerHTML = `${timeResult.hours}h ${timeResult.minutes}m`
            attendDay.innerHTML = `${data.attendance}일`;
            
            if (data.subscription == false) {
                subscribe.innerHTML = `이용권 없음<br/><p>이용권 구매하기</p>`
                subscribe.getElementsByTagName('p')[0].style.fontSize = '1.25rem';
                subscribe.getElementsByTagName('p')[0].style.fontFamily = 'Pretendard-Medium';
                subscribe.getElementsByTagName('p')[0].style.color = 'rgba(255,255,255,0.7)';
            }
            
        } else {
            console.error("Failed to fetch user info:", response.statusText);
        }
    } catch (error) {
    console.error("Error:", error);
}
});

document.addEventListener("DOMContentLoaded", async function () {
    const token = document.cookie;
    try{
        const response = await fetch("/api/ranking/me/tier", {
            method: "GET",
            headers: {
                "Authorization": token,  // Bearer를 포함한 전체 토큰 값
            },
        });
        if (response.ok) {
            const leugedata = await response.json();

            console.log(leugedata)
            ranking[0].innerHTML = `${leugedata.tier} 리그 `;

        } else {
            console.error("Failed to fetch user info:", response.statusText);
        }
    } catch (error) {
    console.error("Error:", error);
}
});

//푼 퀴즈수.. 모델 어디 있는지 모르겠음ㅠㅠ
// document.addEventListener("DOMContentLoaded", async function () {
//     const token = document.cookie;
//     try{
//         const response = await fetch("/api/ranking/me/tier", {
//             method: "GET",
//             headers: {
//                 "Authorization": token,  // Bearer를 포함한 전체 토큰 값
//             },
//         });
//         if (response.ok) {
//             const leugedata = await response.json();

//             console.log(leugedata)
//             ranking[0].innerHTML = `${leugedata.tier} 리그 `;

//         } else {
//             console.error("Failed to fetch user info:", response.statusText);
//         }
//     } catch (error) {
//     console.error("Error:", error);
// }
// });

