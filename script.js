const upload = document.getElementById("videoUpload")
const video = document.getElementById("videoPlayer")

if(upload){
upload.addEventListener("change",function(){

const file=this.files[0]

if(file){
video.src=URL.createObjectURL(file)
}

})
}

function analyzeVideo(){

// stats simulées

let shots=Math.floor(Math.random()*30)
let passes=Math.floor(Math.random()*120)
let steals=Math.floor(Math.random()*15)
let possession=Math.floor(Math.random()*60)+40

document.getElementById("shots").innerText=shots
document.getElementById("passes").innerText=passes
document.getElementById("steals").innerText=steals
document.getElementById("possession").innerText=possession

generateHeatmap(shots)
generateTimeline()

}

function generateHeatmap(shots){

const canvas=document.getElementById("courtCanvas")
const ctx=canvas.getContext("2d")

canvas.width=400
canvas.height=300

for(let i=0;i<shots;i++){

let x=Math.random()*400
let y=Math.random()*300

ctx.beginPath()
ctx.arc(x,y,8,0,Math.PI*2)
ctx.fillStyle="rgba(255,0,0,0.5)"
ctx.fill()

}

}

function generateTimeline(){

const timeline=document.getElementById("timeline")

timeline.innerHTML=""

let events=[
"Tir réussi",
"Interception",
"Passe décisive",
"Contre",
"Rebond offensif"
]

for(let i=0;i<8;i++){

let minute=Math.floor(Math.random()*40)

let event=events[Math.floor(Math.random()*events.length)]

let div=document.createElement("div")

div.innerText=minute+"' - "+event

timeline.appendChild(div)

}

}
