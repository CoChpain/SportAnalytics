const upload = document.getElementById("videoUpload");
const video = document.getElementById("videoPlayer");

if (upload) {
    upload.addEventListener("change", function () {
        const file = this.files[0];
        if (file) {
            video.src = URL.createObjectURL(file);
        }
    });
}

async function analyzeVideo() {
    const file = upload.files[0];
    if (!file) {
        alert("Merci de sélectionner une vidéo.");
        return;
    }

    const formData = new FormData();
    formData.append("video", file);

    const response = await fetch("http://localhost:5000/analyze", {
        method: "POST",
        body: formData
    });

    const data = await response.json();

    document.getElementById("shots").innerText = data.shots;
    document.getElementById("passes").innerText = data.passes;
    document.getElementById("steals").innerText = data.steals;
    document.getElementById("possession").innerText = data.possession;

    generateHeatmapFromPositions(data.shots_positions);
    generateTimelineFromEvents(data.events);
}

function generateHeatmapFromPositions(positions) {
    const canvas = document.getElementById("courtCanvas");
    const ctx = canvas.getContext("2d");

    canvas.width = 400;
    canvas.height = 300;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    positions.forEach(pos => {
        const x = pos.x * canvas.width;
        const y = pos.y * canvas.height;

        ctx.beginPath();
        ctx.arc(x, y, 8, 0, Math.PI * 2);
        ctx.fillStyle = "rgba(255,0,0,0.5)";
        ctx.fill();
    });
}

function generateTimelineFromEvents(events) {
    const timeline = document.getElementById("timeline");
    timeline.innerHTML = "";

    events.forEach(ev => {
        const div = document.createElement("div");
        div.innerText = `${ev.time.toFixed(1)}s - ${ev.type}`;
        timeline.appendChild(div);
    });
}
