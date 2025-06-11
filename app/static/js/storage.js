import { showToast } from "./main.js"

document.addEventListener("DOMContentLoaded", async function () {
    const diskTotal = document.getElementById("disk-total")
    const diskUsed = document.getElementById("disk-used")
    const diskFree = document.getElementById("disk-free")
    const folders  = document.getElementById("folder-count")
    const pictures = document.getElementById("picture-count")

    const log = document.getElementById("log") 

    // Get storage information and display
    const storageResponse = await fetch("/configuration/storage", {
        method: "GET" 
    }) 

    const storageData = await storageResponse.json() 

    if (storageData.status === "success"){
        diskTotal.innerHTML = `${storageData.message.total} GB`
        diskUsed.innerHTML = `${storageData.message.used} GB`
        diskFree.innerHTML = `${storageData.message.free} GB`
        folders.innerHTML = `${storageData.message.folder}`
        pictures.innerHTML = `${storageData.message.file}`
    }
})