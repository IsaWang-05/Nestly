// References: 
    // https://developer.mozilla.org/en-US/docs/Web/API/FormData
    // https://reqbin.com/code/javascript/wc3qbk0b/javascript-fetch-json-example
    // https://stackoverflow.com/questions/9855656/how-can-i-submit-a-form-using-javascript


// base URL
var apiBaseUrl = window.location.origin;

// function to convert form data to a query string
function formDataToQueryString(formData) {
    var params = '';
    for (var pair of formData.entries()) {
        if (pair[1]) {
            params += encodeURIComponent(pair[0]) + '=' + encodeURIComponent(pair[1]) + '&';
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