// base URL
var apiBaseUrl = 'https://eqfosdyv30.execute-api.us-east-1.amazonaws.com/v1';

// convert form data to a query string
function formDataToQueryString(formData) {
    var params = '';
    for (var pair of formData.entries()) {
        if (pair[1]) {
            params += pair[0] + '=' + encodeURIComponent(pair[1]) + '&';
        }
    }
    return params.slice(0, -1);
}

// filter properties
document.getElementById('filterPropertiesForm').onsubmit = function(event) {
    event.preventDefault();
    var formData = new FormData(event.target);
    getProperties(formData);
};

// get all properties
document.getElementById('getAllPropertiesButton').onclick = function() {
    getProperties();
};

// get properties (for filter properties & get all properties)
function getProperties(formData = null) {
    var url = apiBaseUrl + '/properties';
    if (formData) {
        url += '?' + formDataToQueryString(formData);
    }
    fetch(url)
        .then(function(response) {
            return response.json();
        })
        .then(function(data) {
            var resultContainer = document.getElementById('getPropertiesResult');
            resultContainer.innerHTML = '';
            if (Array.isArray(data) && data.length > 0) {
                data.forEach(function(property) {
                    var propertyString = 'ID: ' + property.property_id + ', Address: ' + property.property_address + ', Type: ' + property.house_type + ', Size: ' + property.house_size + ', Price: ' + property.price + ', Availability: ' + property.availability + ', Host ID: ' + property.host_id;
                    var propertyDiv = document.createElement('div');
                    propertyDiv.textContent = propertyString;
                    resultContainer.appendChild(propertyDiv);
                });
            } else {
                resultContainer.textContent = 'No (such) properties were found';
            }
        })
        .catch(function(error) {
            console.error('Error:', error);
        });
}

// create a property (POST)
document.getElementById('createPropertyForm').onsubmit = function(event) {
    event.preventDefault();
    var formData = new FormData(event.target);
    var propertyData = {};
    formData.forEach(function(value, key) {
        propertyData[key] = value;
    });

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
};

// update a property (PUT)
document.getElementById('updatePropertyForm').onsubmit = function(event) {
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
};

// delete a property (DELETE)
document.getElementById('deletePropertyForm').onsubmit = function(event) {
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
};
