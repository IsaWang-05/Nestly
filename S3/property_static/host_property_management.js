// Define the base URL for the API
var apiBaseUrl = 'https://eqfosdyv30.execute-api.us-east-1.amazonaws.com/v1';
var urlParams = new URLSearchParams(window.location.search);
var hostId = urlParams.get('host_id'); // Get hostId from URL

// Fetch and display properties when the page loads
document.addEventListener('DOMContentLoaded', function() {
    fetchProperties(hostId);
});

// Function to fetch properties based on host ID
function fetchProperties(hostId, formData = null) {
    var url = apiBaseUrl + '/properties?host_id=' + encodeURIComponent(hostId);
    if (formData) {
        url += '&' + formDataToQueryString(formData);
    }
    fetch(url)
        .then(response => response.json())
        .then(properties => displayProperties(properties))
        .catch(error => console.error('Error:', error));
}

// Function to display properties in a table
function displayProperties(properties) {
    console.log(properties);
    var resultContainer = document.getElementById('propertiesResult');
    resultContainer.innerHTML = '';

    if (Array.isArray(properties) && properties.length > 0) {
        properties.forEach(function(property) {
            var row = resultContainer.insertRow();
            row.insertCell(0).textContent = property.property_id;
            row.insertCell(1).textContent = property.property_address;
            row.insertCell(2).textContent = property.house_type;
            row.insertCell(3).textContent = property.house_size;
            row.insertCell(4).textContent = property.price;
            row.insertCell(5).textContent = property.availability;
        });
    } else {
        resultContainer.innerHTML = '<tr><td colspan="6">No properties found</td></tr>';
    }
}

// Event listener for Create Property form submission
document.getElementById('createPropertyForm').addEventListener('submit', function(event) {
    event.preventDefault();
    var formData = new FormData(event.target);
    var propertyData = {};
    formData.forEach(function(value, key) {
        propertyData[key] = value;
    });
    propertyData["host_id"] = hostId;

    fetch(apiBaseUrl + '/properties', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(propertyData),
    })
    .then(async function(response) {
        var data = await response.json();

        // failed
        if (!response.ok) {
            var errorMessage = 'Failed to update property';

            if (data && data.detail) {
                errorMessage = data.detail;
            }
            throw new Error(errorMessage);
        }

        alert('Property updated successfully');
    })
    .catch(function(error) {
        alert(error.message);
        console.error('Error:', error);
    });
});

// Event listener for Update Property form submission
document.getElementById('updatePropertyForm').addEventListener('submit', function(event) {
    event.preventDefault();
    var formData = new FormData(event.target);
    var propertyId = formData.get('property_id');
    formData.delete('property_id');

    var propertyData = {};
    formData.forEach(function(value, key) {
        if (value) propertyData[key] = value;
    });

    fetch(apiBaseUrl + '/properties/' + propertyId, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(propertyData),
    })
    .then(async function(response) {
        var data = await response.json();

        // failed
        if (!response.ok) {
            var errorMessage = 'Failed to update property';

            if (data && data.detail) {
                errorMessage = data.detail;
            }
            throw new Error(errorMessage);
        }

        alert('Property updated successfully');
    })

    .catch(function(error) {
        alert(error.message);
        console.error('Error:', error);
    });
});

// Event listener for Delete Property form submission
document.getElementById('deletePropertyForm').addEventListener('submit', function(event) {
    event.preventDefault();
    var propertyId = document.getElementById('deletePropertyId').value;
    fetch(apiBaseUrl + '/properties/' + propertyId, {
        method: 'DELETE',
    })
    .then(function(response) {
        return response.json();
    })
    .then(function(data) {
        alert('Property deleted');
    })
    .catch(function(error) {
        alert('Error deleting property');
        console.error('Error:', error);
    });
});