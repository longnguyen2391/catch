capture_button = document.getElementById("capture-button")
image_container = document.getElementById("image-container") 

capture_button.addEventListener("click", async () => {
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

            image_container.innerHTML = "";
            image_container.style.opacity = "1";
            image_container.appendChild(img);
        } 
        else { 
            alert(data.message);
        }
    }
    catch (err) {
        console.error(err);
    }
})