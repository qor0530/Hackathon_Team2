document.addEventListener("DOMContentLoaded", function () {
  const links = document.querySelectorAll(".sidebar ul li a");

  links.forEach((link) => {
    link.addEventListener("click", function (event) {
      // 모든 링크에서 active 클래스 제거
      links.forEach((link) => link.classList.remove("active"));

      // 클릭된 링크에 active 클래스 추가
      this.classList.add("active");
    });
  });
});
