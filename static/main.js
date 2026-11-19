const fileInput = document.getElementById("image");
const fileLabel = document.getElementById("file-label");
const dropZone = document.getElementById("drop-zone");
const form = document.getElementById("art-form");
const generateButton = document.getElementById("generate-btn");

fileInput.addEventListener("change", () => {
  fileLabel.textContent = fileInput.files.length ? fileInput.files[0].name : "Drop an image here or browse";
});

["dragenter", "dragover"].forEach(eventName => {
  dropZone.addEventListener(eventName, event => {
    event.preventDefault();
    dropZone.classList.add("dragover");
  });
});
["dragleave", "drop"].forEach(eventName => {
  dropZone.addEventListener(eventName, event => {
    event.preventDefault();
    dropZone.classList.remove("dragover");
  });
});
dropZone.addEventListener("drop", event => {
  if (event.dataTransfer.files.length) {
    fileInput.files = event.dataTransfer.files;
    fileLabel.textContent = fileInput.files[0].name;
  }
});
form.addEventListener("submit", () => {
  generateButton.disabled = true;
  generateButton.querySelector("span").textContent = "Generating artwork...";
});
