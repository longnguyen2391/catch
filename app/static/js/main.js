document.addEventListener("DOMContentLoaded", async function () {
    try { 
        const response = await fetch('/timelapse/config', {
            method: "GET"
        })

        const data = await response.json();
                
        const autoStart = document.getElementById("auto-start");

        if (data.message.enable === "true"){
            autoStart.checked = true; 

            await enableTimelapse(data);
        }
        else {
            autoStart.checked = false;
        }

        async function enableTimelapse(configData) { 
            const formData = new FormData(); 

            formData.append("minutes", configData.message.minutes);
            formData.append("second", configData.message.second);
            formData.append("enable", true);

            const response = await fetch('/timelapse/start', {
                method: "POST", 
                body: formData
            })

            const data = await response.json();

            if (data.status === "success"){
                timelapseStatus = document.getElementById("timelapse-status");
                timelapseStatus.innerHTML = ""; 
                timelapseStatus.innerHTML = data.message; 
            } 
        }
    }
    catch (err) {
        console.log(err);
    }   
})