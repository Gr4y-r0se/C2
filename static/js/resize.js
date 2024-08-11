
function changeText() {

    var screenWidth = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;

    var textElement = document.getElementById("nav-title");

    if (screenWidth < 769) {
        textElement.innerHTML = "C2";
        //nav_image.height = 40;
        //nav_image.width = 44; 
    } else {
        textElement.innerHTML = "Connect and Control";
        //nav_image.height = 200;
        //nav_image.width = 220; 
    }
}
    
window.addEventListener('load', changeText);
window.addEventListener('resize', changeText);