document.addEventListener("DOMContentLoaded", function() {
  const loginBtn = document.getElementById("login-btn");

  loginBtn.addEventListener("click", async function(event) {
      event.preventDefault();

      const username = document.querySelector(".id-input").value;
      const password = document.querySelector(".password-input").value;

      const response = await fetch("/api/user/login", {
          method: "POST",
          headers: {
              "Content-Type": "application/x-www-form-urlencoded",
          },
          body: new URLSearchParams({
              username: username,
              password: password,
          }),
      });

      if (response.ok) {
          const data = await response.json();
          console.log("Token stored in cookie");  // 토큰이 쿠키에 저장됨을 확인
          window.location.href = "/";  // 로그인 후 메인 페이지로 이동
      } else {
          console.error("Login failed:", response.statusText);
          alert("로그인 실패: 아이디 또는 비밀번호를 확인하세요.");
      }
  });
});
