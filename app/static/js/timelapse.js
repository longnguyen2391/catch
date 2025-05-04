startButton = document.getElementById("timelapse-start-button");
endButton = document.getElementById("timelapse-end-button"); 
autoStart = document.getElementById("auto-start");
timelapseStatus = document.getElementById("timelapse-status");

// Handle timelapse is working or not? 
document.addEventListener("DOMContentLoaded", async function () {
    try { 
        const response = await fetch("/timelapse/status", {
            method: "GET"
        })

        const data = await response.json() 

        timelapseStatus.innerHTML = ""; 
        timelapseStatus.innerHTML = data.message; 
    } catch (err) {
        console.log(err)
    }
})

// Handle start timelapse button
startButton.addEventListener("click", async function () {
    const minutes = document.getElementById("minutes").value;  
    const second = document.getElementById("second").value; 
    const formData = new FormData(); 
    
    formData.append("minutes", minutes);
    formData.append("second", second);
    
    if (!autoStart.checked){
        formData.append("enable", false);
    }
    else {
        formData.append("enable", true);
    }

    try {
        const response = await fetch('/timelapse/start', {
            method: "POST", 
            body: formData
        }) 

        const data = await response.json(); 

        alert(data.message);

        if (data.status === "success") {
            timelapseStatus.innerHTML = ""; 
            timelapseStatus.innerHTML = data.message; 
        } 
    } 
    catch (err){
        console.log(err);
    }
})

// Handle stop timelapse button
endButton.addEventListener("click", async function () {
    try {
        const response = await fetch("/timelapse/end", {
            method: "GET" 
        })

        const data = await response.json(); 

        alert(data.status) 

        if (data.status === "success") {
            timelapseStatus.innerHTML = ""; 
            timelapseStatus.innerHTML = "Stop"; 
        } 
    }
    catch (err){
        console.log(err);
    }
})