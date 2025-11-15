
document.addEventListener('DOMContentLoaded', () => {

    const foodDrop = document.getElementById('foodDrop');
    const foodImg = document.getElementById('foodImg');

    // this varible will be changed with what the html doc has
    const textData = document.getElementById('textData');
    
    foodDrop.addEventListener('dragover', (event) => {
        event.preventDefault();
        foodDrop.classList.add('dragover');
    });


        const formData = new FormData('textData');

        fetch("/analyze",{
            method: "POST",
            body: formData
        })
        //this will be directed to the backend of the file to have it analyzed

        .then(response => response.json()
   
        }.then(data => {
            console.log(data);

            // this needs to be changed to what the html file for the repose is 
            textData.textContent = data.analysis;


        )


})

