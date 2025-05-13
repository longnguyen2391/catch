import { showToast } from "./main.js"

document.addEventListener("DOMContentLoaded", function () {
    const capture = document.getElementById("capture") 

    capture.addEventListener("click", async function () {
        const response = await fetch("/capture/preview", {
            method: "POST"
        })

        const data = await response.json() 
        console.log(data)
        if (data.status === "success"){
            const image = document.createElement("img")
            const container = document.querySelector(".content__image")
            const containerRect = container.getBoundingClientRect()

            container.innerHTML = ""
            container.style.opacity = "1"

            image.src = data.message; 
            image.width = containerRect.width; 
            image.height = containerRect.height;

            container.appendChild(image)
        }

        showToast(data.message)
    })
})