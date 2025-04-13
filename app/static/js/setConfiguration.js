document.addEventListener("DOMContentLoaded", function () {
    const selects = document.querySelectorAll("select"); 

    selects.forEach(select => {
        select.addEventListener("change", async function () {
            const formData = new FormData(); 
            formData.append(this.name, this.value); 

            try {
                const response = await fetch("/configuration/set",{
                    method: "POST",
                    body: formData
                })

                const data = response.json()  
                
                alert(data.status, data.message)
            } 
            catch (err) {
                console.log(err)
            }
        });
    });
});