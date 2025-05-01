document.addEventListener("DOMContentLoaded", async function () {
    try {
        const response = await fetch('/configuration/storage-info', {
            method: "GET"
        })

        const data = await response.json();

        console.log(data.message)
        
        folderElement = document.getElementById("current-folder-count");
        fileElement = document.getElementById("current-file-count");
        diskCapacity = document.getElementById("disk-capacity");
        diskUsed = document.getElementById("disk-used");
        freeSpace = document.getElementById("free-space");


        diskCapacity.innerHTML = data.message.total + "GB"; 
        diskUsed.innerHTML = data.message.used + "GB"; 
        freeSpace.innerHTML = data.message.free + "GB"; 
        folderElement.innerHTML = data.message.folder;
        fileElement.innerHTML = data.message.file;
    }
    catch (err) {
        console.log(err);
    }
})

const syncButton = document.getElementById("manual-sync") 

syncButton.addEventListener("click", async function () {
    try { 
        const response = await fetch('/configuration/sync', {
            method: "POST"
        })

        const data = await response.json() 

        alert(data.message)
    }
    catch (err) {
        console.log(err)
    }
})