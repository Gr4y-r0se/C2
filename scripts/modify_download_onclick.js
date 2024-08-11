function newDownloadFunction(event) {
    event.preventDefault();
    alert('Download button hijacked');
}

const buttons = document.querySelectorAll(['button','a']);

buttons.forEach(button => {
    if (button.textContent.trim().toLowerCase().includes('download')) {
        button.onclick = newDownloadFunction;
    }
});
