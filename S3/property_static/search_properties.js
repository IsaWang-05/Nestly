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
document.getElementById('searchPropertiesForm').addEventListener('submit', function (e) {
    e.preventDefault();
    const formData = new FormData(this);
    const queryString = formDataToQueryString(formData);
    getProperties(queryString);
});

// get properties (for filter properties & get all properties)
function getProperties(queryString = '') {
    var url = apiBaseUrl + '/properties';
    if (queryString) {
        url += '?' + queryString;
    }
    fetch(url)
        .then(function(response) {
            return response.json();
        })
        .then(function(data) {
            var resultContainer = document.getElementById('searchResults');
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
