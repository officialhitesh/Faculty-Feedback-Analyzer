const fileInput = document.getElementById('file-upload');
const uploadImg = document.getElementById('upload-img');
const fileNameDisplay = document.getElementById('file-name');
const submitBtn = document.getElementById('submit-btn'); // new button

// File browser
uploadImg.addEventListener('click', () => {
    fileInput.click();
});

// Show selected file name and button
fileInput.addEventListener('change', () => {
    if (fileInput.files.length > 0) {
        fileNameDisplay.textContent = "📂 Selected File: " + fileInput.files[0].name;
        submitBtn.style.display = "inline-block"; // show button
    } else {
        fileNameDisplay.textContent = "";
        submitBtn.style.display = "none"; // hide button if no file
    }
});
