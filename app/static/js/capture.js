document.addEventListener("DOMContentLoaded", function () {
    const capture = document.getElementById("capture") 

    capture.addEventListener("click", async function () {
        const response = await fetch("/capture/preview", {
            method: "POST"
        })

        const data = await response.json() 

        if (data.status === "success"){
            const image = document.createElement("img")
            const container = document.querySelector(".content__image")
            const containerRect = container.getBoundingClientRect()

            container.innerHTML = ""

            image.src = data.message; 
            image.width = containerRect.width; 
            image.height = containerRect.height;

            container.appendChild(image)
        }
    })
})