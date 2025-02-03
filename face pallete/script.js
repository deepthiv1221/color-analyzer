const video = document.getElementById('video');
const startTest = document.getElementById('start-test');
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const leftHand = document.getElementById('left-hand');
const rightHand = document.getElementById('right-hand');
const palettes = document.querySelectorAll('.palette');

startTest.addEventListener('click', () => {
    navigator.mediaDevices.getUserMedia({ video: true })
        .then((stream) => {
            video.srcObject = stream;
        })
        .catch((err) => {
            console.error("Error accessing webcam: ", err);
        });

    setTimeout(analyzeImage, 5000); // Take a picture after 5 seconds
});

async function analyzeImage() {
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    
    canvas.toBlob(async (blob) => {
        const formData = new FormData();
        formData.append("image", blob, "image.jpg");

        const response = await fetch("http://127.0.0.1:5000/analyze", {
            method: "POST",
            body: formData
        });

        const result = await response.json();
        updatePalettes(result.best); // Update the displayed palettes based on result
    }, 'image/jpeg');
}

function updatePalettes(bestColors) {
    // Update the color palettes based on the analysis result
    palettes.forEach((palette, index) => {
        if (bestColors[index]) {
            palette.style.backgroundColor = bestColors[index];
        }
    });
}
