const swup = new Swup();


function toggleDesc(id){
    let description = document.getElementById(id)

    if (description.style.display === 'block'){
        description.style.display = 'none'
    }
    else{
        description.style.display = 'block'
    }
}