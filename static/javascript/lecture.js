document.addEventListener("DOMContentLoaded", function () {
  var element = document.getElementById("go-to-subject-select");
  if (element) {
    element.addEventListener("click", function () {
      window.location.href = "/lecture/subject";
    });
  }
});

document.addEventListener("DOMContentLoaded", function () {
  var element = document.getElementById("go-to-study-write");
  if (element) {
    // 1~10 사이 난수 생성 후 넣기
    var random = Math.floor(Math.random() * 10) + 1;
    element.addEventListener("click", function () {
      window.location.href = `/lecture/write/${random}`;
    });
  }
});

document.addEventListener("DOMContentLoaded", function () {
  var element = document.getElementById("go-to-study-situation");
  if (element) {
    // 1~10 사이 난수 생성 후 넣기
    var random = Math.floor(Math.random() * 10) + 1;
    element.addEventListener("click", function () {
      window.location.href = `/lecture/situation/${random}`;
    });
  }
});
