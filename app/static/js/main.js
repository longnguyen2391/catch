// Load information and configuration data to frontend
document.addEventListener("DOMContentLoaded", async function () {
    // Information
    const camera = document.getElementById("camera") 
    const battery = document.getElementById("battery")
    const shuttercount = document.getElementById("shuttercount")
    const lens = document.getElementById("lens")

    // Configuration current value
    const iso = document.getElementById("iso")
    const shutterspeed = document.getElementById("shutterspeed")
    const aperture = document.getElementById("aperture")
    const whitebalance = document.getElementById("whitebalance")
    const autoexposuremode = document.getElementById("autoexposuremode")
    const focusmode = document.getElementById("focusmode")

    // Selects of configuration
    const isoChoices = iso.nextElementSibling
    const shutterspeedChoices = shutterspeed.nextElementSibling
    const apertureChoices = aperture.nextElementSibling
    const whitebalanceChoices = whitebalance.nextElementSibling
    const autoexposuremodeChoices = autoexposuremode.nextElementSibling
    const focusmodeChoices = focusmode.nextElementSibling

    const choiceMap = [
        { key: "iso", select: isoChoices },
        { key: "shutterspeed", select: shutterspeedChoices },
        { key: "aperture", select: apertureChoices },
        { key: "whitebalance", select: whitebalanceChoices },
        { key: "autoexposuremode", select: autoexposuremodeChoices },
        { key: "focusmode", select: focusmodeChoices },
    ];

    const response = await fetch("/configuration/get",{
        method: "GET"
    }) 

    const data = await response.json()

    if (data.status === "success") {
        camera.innerHTML = data.message.cameramodel.current_value;
        battery.innerHTML = data.message.batterylevel.current_value;
        shuttercount.innerHTML = data.message.shuttercounter.current_value;
        lens.innerHTML = data.message.lensname.current_value;
    
        iso.innerHTML = data.message.iso.current_value;
        shutterspeed.innerHTML = data.message.shutterspeed.current_value;
        aperture.innerHTML = data.message.aperture.current_value;
        whitebalance.innerHTML = data.message.whitebalance.current_value;
        autoexposuremode.innerHTML = data.message.autoexposuremode.current_value;
        focusmode.innerHTML = data.message.focusmode.current_value;
        
        // Append options for each select
        choiceMap.forEach(({ key, select }) => {
            const choices = data.message[key]?.choices || [];
            choices.forEach(choice => {
                const option = document.createElement("option");
                option.value = choice;
                option.textContent = choice;
                select.appendChild(option);
            });
        });
    }

    // If any value change in select it will call set new configuration api
    choiceMap.forEach(({ select }) => {
        select.addEventListener("change", async function () {
            const requestData = new FormData() 
            requestData.append(this.name, this.value)

            const response = await fetch("/configuration/set", {
                method: "POST", 
                body: requestData
            })

            const data = await response.json() 

            if (data.status === "success"){
                const config = document.getElementById(`${this.name}`)
                config.innerHTML = this.value

                showToast(`${data.message}`)
            }
        })
    })
})

export function showToast(message) {
    const toast = document.querySelector(".toast")
    toast.innerHTML = message
    toast.classList.add("toast--display")

    setTimeout(() => {
        toast.classList.remove("toast--display")
        toast.innerHTML = ""
    }, 4000)
}