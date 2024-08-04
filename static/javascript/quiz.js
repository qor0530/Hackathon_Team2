document.addEventListener("DOMContentLoaded", () => {
  document
    .querySelector(".answer-button")
    .addEventListener("click", async () => {
      const response = await fetch("/api/quiz");
      const data = await response.json();
      console.log(data);
      // 데이터 처리 및 화면 업데이트
      document.querySelector(".quiz-question .blank").innerText = data.answer;
    });
});
