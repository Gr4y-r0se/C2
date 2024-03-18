
function changeText() {

    var screenWidth = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;

    var textElement = document.getElementById("nav-title");

    if (screenWidth < 769) {
        textElement.innerHTML = "C2";
    } else {
        textElement.innerHTML = "Connect and Control";
    }
}
    
window.addEventListener('load', changeText);
window.addEventListener('resize', changeText);