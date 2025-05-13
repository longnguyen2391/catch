import { showToast } from "./main.js"

document.addEventListener("DOMContentLoaded", async function () {
    // Display information tags
    const timelapseStatus = document.getElementById("timelapse-status")
    const autoStatus = document.getElementById("auto-status")    
    const duration = document.getElementById("duration") 
    const auto = document.getElementById("auto")

    // Button
    const start = document.getElementById("start")
    const end = document.getElementById("end")

    // Handle start timelapse button 
    start.addEventListener("click", async function () {
        const minutes = document.getElementById("minutes").value 
        const second = document.getElementById("seconds").value
        const interval = (Number(minutes) * 60) + Number(second)

        const formData = new FormData()
        
        formData.append("minutes", minutes)
        formData.append("second", second)
        
        if (!auto.checked){
            formData.append("enable", false)
        }
        else {
            formData.append("enable", true)
        }

        const response = await fetch("/timelapse/start", {
            method: "POST", 
            body: formData
        })

        const data = await response.json()

        if (data.status === "success"){
            timelapseStatus.innerHTML = "Active"
            duration.innerHTML = `${interval} (s)`
            showToast(`${data.message}`)
        }
    })

    // Handle end timelapse button 
    end.addEventListener("click", async function () {
        const response = await fetch("/timelapse/end", {
            method: "GET" 
        })

        const data = await response.json()

        if (data.status === "success") { 
            timelapseStatus.innerHTML = "Inactive"
            showToast(`${data.message}`)
        }
    })

    const statusResponse = await fetch("/timelapse/status", {
        method: "GET" 
    })
    const configResponse = await fetch("/timelapse/config", {
        method: "GET"
    })

    const statusData = await statusResponse.json()
    const configData = await configResponse.json()

    // Timelapse
    if (statusData.status === "success"){
        if (statusData.message === "True"){
            timelapseStatus.innerHTML = "Active"
        } else {
            timelapseStatus.innerHTML = "Inactive"
        }
    }  

    // Config
    if (configData.status === "success"){
        if (configData.message.enable === "true"){
            autoStatus.innerHTML = "Enable"
            auto.checked = true
        } else {
            autoStatus.innerHTML = "Disable"
            auto.checked = false
        }

        // Calculate duration from config
        let seconds = (Number(configData.message.minutes) * 60) + Number(configData.message.second)
        duration.innerHTML = `${seconds} (s)`
    }

    async function enableTimelapse(configData) {
        const formData = new FormData()
        
        formData.append("minutes", configData.message.minutes)
        formData.append("second", configData.message.second)
        formData.append("enable", true)

        const response = await fetch("/timelapse/start", {
            method: "POST", 
            body: formData
        })

        const data = await response.json()

        if (data.status === "success"){
            timelapseStatus.innerHTML = "Active"
        }
    }
}) 