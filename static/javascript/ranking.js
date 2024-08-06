document.addEventListener("DOMContentLoaded", function () {
    const infoMark = document.getElementById("info-mark");

    infoMark.addEventListener("mouseover", function () {
        const tooltip = this.querySelector(".tooltip");
        tooltip.style.display = "block";
    });

    infoMark.addEventListener("mouseout", function () {
        const tooltip = this.querySelector(".tooltip");
        tooltip.style.display = "none";
    });
});