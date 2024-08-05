document.addEventListener("DOMContentLoaded", () => {
  const quizBoxes = document.querySelectorAll(".quiz-box");

  const showModal = (message) => {
    const modal = document.createElement("div");
    modal.classList.add("modal");
    modal.innerHTML = `
      <div class="modal-content">
        <span class="close-button">&times;</span>
        <p>${message}</p>
      </div>
    `;
    document.body.appendChild(modal);

    const closeButton = modal.querySelector(".close-button");
    closeButton.addEventListener("click", () => {
      modal.remove();
    });

    modal.addEventListener("click", (event) => {
      if (event.target === modal) {
        modal.remove();
      }
    });
  };

  const getUserId = async () => {
    try {
      const response = await fetch("/api/user/me", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        throw new Error("Failed to fetch user info");
      }

      const user = await response.json();
      return user.id;
    } catch (error) {
      console.error("Error fetching user ID:", error);
      showModal("사용자 정보를 가져오는데 실패했습니다.");
    }
  };

  quizBoxes.forEach((box) => {
    box.addEventListener("click", async () => {
      const quizTitle = box.querySelector(".quiz-title").textContent;
      let quizType;

      if (quizTitle.includes("오늘의 퀴즈 풀기")) {
        quizType = "random";
      } else if (quizTitle.includes("틀린 퀴즈 풀기")) {
        quizType = "incorrect";
      } else if (quizTitle.includes("내 레벨 대 퀴즈 풀기")) {
        quizType = "level";
      } else {
        return;
      }

      const userId = await getUserId(); // API를 통해 user_id를 얻어옴
      if (!userId) return;

      if (quizType === "level") {
        // 비슷한 레벨의 퀴즈를 가져옴
        const response = await fetch(`/api/quiz/similar_level_quizzes/${userId}`, {
          method: "GET",
        }).catch((error) => console.error("Error fetching similar level quizzes:", error));
        
        if (response.ok) {
          const data = await response.json();
          console.log("Quiz stack:", data.quiz_stack);
        } else {
          showModal("비슷한 레벨의 퀴즈를 가져오는데 실패했습니다.");
          return;
        }
      }

      // Start quiz and update quiz_stack
      const response = await fetch(
        `/api/quiz/next_quiz/${userId}`,
        {
          method: "GET",
        }
      ).catch((error) => console.error("Error starting quiz:", error));

      if (response.redirected) {
        window.location.href = response.url;
      } else {
        const result = await response.json();
        if (result.error === "quiz_stack_empty") {
          showModal("퀴즈 스택이 비어 있습니다.");
        } else {
          console.error("Failed to start quiz", result);
        }
      }
    });
  });
});
