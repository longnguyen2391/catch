captureButton = document.getElementById("capture-button")
imageContainer = document.getElementById("image-container") 

captureButton.addEventListener("click", async () => {
    try {
        const response = await fetch("/capture/preview", {
            method: "POST"
        }); 

        const data = await response.json(); 

        if (data.status === "success") {
            const img = document.createElement('img'); 
            img.src = data.message; 
            img.width = 300; 
            img.height = 240; 

            imageContainer.innerHTML = "";
            imageContainer.style.opacity = "1";
            imageContainer.appendChild(img);
        } 
        else { 
            alert(data.message);
        }
    }
    catch (err) {
        console.error(err);
    }
})