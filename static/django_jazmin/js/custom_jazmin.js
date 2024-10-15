document.addEventListener("DOMContentLoaded", function() {
    var navItem = document.querySelectorAll('.nav-item.d-none');
    navItem.forEach((item)=>{
        if(item){
            item.classList.remove('d-none');
        }
    })
});
