async function populateEndpoints() {
    try {
        // Fetch data from the server
        const response = await fetch('/endpoints/list');
        
        // Check if the response is ok
        if (!response.ok) {
            throw new Error(`Error: ${response.statusText}`);
        }

        // Parse the response as JSON
        const data = await response.json();

        // Get the container where the accordion elements will be placed
        const container = document.getElementById('endpoint_container');
        
        // Clear existing content in the container
        container.innerHTML = '';

        // Iterate over the data to create accordion elements
        data.forEach((endpoint, index) => {
            const accordionItem = `
                <div class="accordion-item">
                    <div class="accordion-header" id="heading${index}" aria-expanded="false">
                         <div class="accordion-title">
                            ${endpoint.name}
                        </div>
                         <div class="button-container">
                            <button class="edit-button" type="button" onclick="editEndpoint('${endpoint.uuid}')">Edit</button>
                            <button class="delete-button" type="button" onclick="deleteEndpoint('${endpoint.uuid}')">Delete</button>
                        </div>
                    </div>
                    <div id="collapse${index}" class="accordion-body">
                        <p><strong>Endpoint:</strong> ${location.protocol.concat('//',location.hostname,'/e/',endpoint.endpoint)}</p>
                        <p><strong>Description:</strong> ${endpoint.description}</p>
                        <p><strong>Method:</strong> ${endpoint.method}</p>
                        <p><strong>Payload:</strong> ${endpoint.payload}</p>
                    </div>
                </div>
            `;

            // Append the generated accordion item to the container
            container.innerHTML += accordionItem;
        });

        // Add event listeners to the buttons for toggling the accordion sections
        const accordionButtons = document.querySelectorAll('.accordion-header');
        accordionButtons.forEach(button => {
            button.addEventListener('click', function () {
                // Toggle the active class on the clicked button
                const isActive = button.getAttribute('aria-expanded') === 'true';
                button.setAttribute('aria-expanded', !isActive);
                button.classList.toggle('active');

                // Toggle the visibility of the corresponding accordion body
                const body = button.nextElementSibling;
                if (isActive) {
                    body.style.display = 'none';
                } else {
                    body.style.display = 'block';
                }
            });
        });

    } catch (error) {
        console.error('Failed to fetch and populate endpoints:', error);
    }
}

function editEndpoint(endpointId) {
    // Open the modal
    const modal = document.getElementById('editModal');
    modal.style.display = "block";

    // Fetch the endpoint data (simulate this with a fetch request to your backend)
    fetch(`/endpoints/data?id=${endpointId}`)
        .then(response => response.json())
        .then(data => {
            // Populate the form fields with data
            document.getElementById('endpoint_id').value = data.uuid;
            document.getElementById('endpoint_name').value = data.name;
            document.getElementById('endpoint_description').value = data.description;
            document.getElementById('endpoint_url').value = data.endpoint;
            document.getElementById('endpoint_method').value = data.method;
            populatePresavedOptions(data.payload);
            setSelect('endpoint_method',data.method)
            // You can also populate the payload dropdown if needed
        })
        .catch(error => console.error('Error fetching endpoint data:', error));
}

// Function to close the modal
function closeModal() {
    const modal = document.getElementById('editModal');
    modal.style.display = "none";
}

async function save_endpoint() {

    const endpointId = document.getElementById('endpoint_id').value;
    const endpointName = document.getElementById('endpoint_name').value;
    const endpointUrl = document.getElementById('endpoint_url').value;
    const endpointDescription = document.getElementById('endpoint_description').value;
    const endpointMethod = document.getElementById('endpoint_method').value;
    const endpointPayload = document.getElementById('endpoint_payload').value;

    if (!endpointName || !endpointUrl ) {
        alert('Please ensure all inputs are filled.');
        return;
    }
    const formData = new FormData();
    formData.append('name', endpointName);
    formData.append('uuid', endpointId);
    formData.append('description', endpointDescription);
    formData.append('endpoint', endpointUrl);
    formData.append('payload', endpointPayload);
    formData.append('method', endpointMethod);


    await fetch('/endpoint/save', {
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
    
    populateEndpoints();

    setTimeout(() => {
        closeModal();
    }, 2000)
}



window.onload = async function() {
    await populateEndpoints()
}

function setSelect(id, savedOption) {
    var selectElement = document.getElementById(id);
    for (let i = 0; i < selectElement.options.length; i++) {
        // If the option value matches the known value, mark it as selected
        if (selectElement.options[i].value === savedOption) {
            selectElement.selectedIndex = i;
            break; // Stop the loop once the correct option is found
        }
    }
}

//Stolen from payloads.js

async function populatePresavedOptions(savedOption) {
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
        const selectElement = document.getElementById('endpoint_payload');
        
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
        newOption.textContent = '--Blank--';
        selectElement.appendChild(newOption);

        setSelect('endpoint_payload',savedOption)
        
    } catch (error) {
        console.error('Failed to fetch and populate options:', error);
    }
}


async function deleteEndpoint(endpointId) {
    try {
        
        const response = await fetch(`/endpoint/delete/${endpointId}`, {
            method: 'DELETE',
        });

        // Parse the JSON response
        const data = await response.json();

        // Check if the delete was successful
        if (response.ok) {
            populateEndpoints();
        } else {
            console.error(`Error: ${result.message}`);
        }
    } catch (error) {
        console.error('Error deleting payload:', error);
    }
}