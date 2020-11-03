const contactInfoButton = document.querySelector("#contact-info-button");
const X = document.querySelector("#hide");
const infoBlock = document.querySelector("#info-block");

function showInfo() {
    infoBlock.classList.remove("transform");
}

function hideInfo() {
    infoBlock.classList.add("transform");
}

contactInfoButton.addEventListener("click", showInfo);
hide.addEventListener("click", hideInfo);