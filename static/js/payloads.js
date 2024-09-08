function setEditorMode(contentType) {
    switch (contentType) {
        case 'text/javascript': // JavaScript content type
            editor.session.setMode(new (ace.require("ace/mode/javascript").Mode)());
            break;
        case 'application/json': // JSON content type
            editor.session.setMode(new (ace.require("ace/mode/json").Mode)());
            break;
        case 'application/xml': // XML content type
            editor.session.setMode(new (ace.require("ace/mode/xml").Mode)());
            break;
        case 'text/html': // HTML content type
            editor.session.setMode(new (ace.require("ace/mode/html").Mode)());
            break;
        default:
            editor.session.setMode(new (ace.require("ace/mode/text").Mode)());
            break;
    }
}


function populate(sel) {
    //document.getElementById('activate_button').innerHTML = 'Set as Active';
    var id = sel.value;
    fetch(`/payload/data?id=${id}`).then(response => {
        if (!response.ok) {
            throw new Error('Server responded with: ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        editor.setValue(data.payload, -1);
        document.getElementById('payload_name').value = data.name;
        document.getElementById('payload_description').value = data.description;
        setEditorMode(data.content_type);
        document.getElementById('payload_content_type').value = data.content_type;
        document.getElementById('uuid').value = id;
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });
    
    return true;
};

async function publish_payload_locally() {
    await fetch('/payload/publish?id='.concat(document.getElementById('uuid').value)).then(response => {return response.json()}).then(data => {
            const button = document.getElementById('publish_button');
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
async function save_payload() {

    const payloadName = document.getElementById('payload_name').value;
    const uuid = document.getElementById('uuid').value;
    const payloadDescription = document.getElementById('payload_description').value;
    const payloadContentType = document.getElementById('payload_content_type').value;
    const payloadContent = editor.getValue();

    if (!payloadName || !payloadContent) {
        alert('Payload name and content are required!.');
        return;
    }
    const formData = new FormData();
    formData.append('name', payloadName);
    formData.append('uuid', uuid);
    formData.append('description', payloadDescription);
    formData.append('content_type', payloadContentType);
    formData.append('the_payload', payloadContent);


    await fetch('/payload/save', {
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
    //Finally, reload the options:
    populatePresavedOptions();
}

window.onload = function() {
    setup()
}

async function setup() {
    // Wait for populatePresavedOptions to finish
    await populatePresavedOptions();

    const dropdown = document.getElementById('presaved');
    dropdown.selectedIndex = 0;
    populate(dropdown);
}

async function populatePresavedOptions() {
    try {
        // Send fetch request to /payload/list
        const response = await fetch('/payload/list');
        
        // Check if the response is ok
        if (!response.ok) {
            throw new Error(`Error: ${response.statusText}`);
        }

        // Parse the response as JSON
        const data = await response.json();
        
        // Get the select element by its id
        const selectElement = document.getElementById('presaved');
        
        // Clear the existing options
        selectElement.innerHTML = '';
        
        // Iterate over the returned keys and create options
        for (let key in data) {
            if (data.hasOwnProperty(key)) {
                // Create a new option element
                const option = document.createElement('option');
                option.value = key;  // Set the value attribute to the key
                option.textContent = data[key];  // Set the displayed text to the key
                
                // Append the option to the select element
                selectElement.appendChild(option);
            }
        }
        
        // Optionally, add a default "New" option
        const newOption = document.createElement('option');
        newOption.value = '';  // Empty value for new option
        newOption.textContent = '--New--';
        selectElement.appendChild(newOption);
        
    } catch (error) {
        console.error('Failed to fetch and populate options:', error);
    }
}



async function delete_payload() {
    try {
        payloadId = document.getElementById('uuid').value;
        const response = await fetch(`/payload/delete/${payloadId}`, {
            method: 'DELETE',
        });

        // Parse the JSON response
        const data = await response.json();

        // Check if the delete was successful
        if (response.ok) {
            button = document.getElementById('delete_button')
            const originalValue = button.innerHTML;
            button.innerHTML = data.response_text;
            button.style['background-color'] = data.colour //Spelt correctly the second time
            setTimeout(() => {
                button.innerHTML = originalValue;
                button.style['background-color'] = '#d9534f'
            }, 5000);
            setup();
        } else {
            console.error(`Error: ${result.message}`);
        }
    } catch (error) {
        console.error('Error deleting payload:', error);
    }
}