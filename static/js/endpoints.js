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
                    <div class="accordion-header" id="heading${index}">
                        <button class="accordion-button" type="button" aria-expanded="false">
                            ${endpoint.name}
                        </button>
                        <button class="edit-button" type="button" onclick="editEndpoint('${endpoint.uuid}')">Edit</button>
                    </div>
                    <div id="collapse${index}" class="accordion-body">
                        <p><strong>Endpoint:</strong> ${location.protocol.concat('//',location.hostname.domain,'/e/',endpoint.endpoint)}</p>
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
        const accordionButtons = document.querySelectorAll('.accordion-button');
        accordionButtons.forEach(button => {
            button.addEventListener('click', function () {
                // Toggle the active class on the clicked button
                const isActive = button.getAttribute('aria-expanded') === 'true';
                button.setAttribute('aria-expanded', !isActive);
                button.classList.toggle('active');

                // Toggle the visibility of the corresponding accordion body
                const body = button.parentElement.nextElementSibling;
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
            // You can also populate the payload dropdown if needed
        })
        .catch(error => console.error('Error fetching endpoint data:', error));
}

// Function to close the modal
function closeModal() {
    const modal = document.getElementById('editModal');
    modal.style.display = "none";
}

// Function to save the edited endpoint
function saveEndpoint() {
    const endpointId = document.getElementById('endpoint_id').value;
    const endpointName = document.getElementById('endpointname').value;
    const endpointUrl = document.getElementById('endpoint_url').value;
    const endpointMethod = document.getElementById('endpoint_method').value;

    // Make a PUT request to update the endpoint data
    fetch(`/endpoints/data/${endpointId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            name: endpointName,
            url: endpointUrl,
            method: endpointMethod
        })
    })
    .then(response => response.json())
    .then(data => {
        alert('Endpoint updated successfully!');
        closeModal();
        // Optionally, reload the page or update the UI to reflect changes
    })
    .catch(error => console.error('Error updating endpoint:', error));
}


window.onload = async function() {
    await populateEndpoints()
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
        newOption.textContent = '--Blank--';
        selectElement.appendChild(newOption);

        for (let i = 0; i < selectElement.options.length; i++) {
            // If the option value matches the known value, mark it as selected
            if (selectElement.options[i].value === savedOption) {
                selectElement.selectedIndex = i;
                break; // Stop the loop once the correct option is found
            }
        }
        
    } catch (error) {
        console.error('Failed to fetch and populate options:', error);
    }
}