function populate(sel) {
    document.getElementById('activate_button').innerHTML = 'Set as Active';
    var id = sel.value;
    fetch(`/script/data?id=${id}`).then(response => {
        if (!response.ok) {
            throw new Error('Server responded with: ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        document.getElementById('the_script').value = data.script;
        document.getElementById('scriptname').value = data.script_name;
        document.getElementById('uuid').value = id;
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });
    
    return true;
};
async function set_script_as_active() {
    await fetch('/script/active?id='.concat(document.getElementById('uuid').value)).then(response => {return response.json()}).then(data => {
            const button = document.getElementById('activate_button');
            const originalValue = button.innerHTML;
            button.innerHTML = data.response_text;
            button.style['background-color'] = data.colour //Spelt correctly the second time
            setTimeout(() => {
                button.innerHTML = originalValue;
                button.style['background-color'] = '#76ABAE'
            }, 5000);
        }).catch(error => {
        console.error('There was a problem with the fetch operation: ', error);
    });
   
    return true;
};
async function save_script() {

    const scriptName = document.getElementById('scriptname').value;
    const uuid = document.getElementById('uuid').value;
    const scriptContent = document.getElementById('the_script').value;

    if (!scriptName || !scriptContent) {
        alert('Script name and content are required!.');
        return;
    }
    const formData = new FormData();
    formData.append('name', scriptName);
    formData.append('uuid', uuid);
    formData.append('the_script', scriptContent);


    await fetch('/script/save', {
        method: 'POST',
        body: formData
    }).then(response => {
        return response.json();
    }).then(data => {
        button = document.getElementById('save_button')
        const originalValue = button.innerHTML;
        button.innerHTML = data.response_text;
        button.style['background-color'] = data.colour //Spelt correctly the second time
        setTimeout(() => {
            button.innerHTML = originalValue;
            button.style['background-color'] = '#76ABAE'
        }, 5000);
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation: ', error);
    });

}

window.onload = function() {
    const dropdown = document.getElementById('presaved')
    dropdown.selectedIndex = 0;
    populate(dropdown);
}