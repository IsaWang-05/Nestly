# NOTE: Please do not play with this api (namely, the create properties / update address field) too much, 
    # Smartystreets only provides 1000 checks/mo and we need to save it for demos. 
    # Thanks!

import requests
from requests.exceptions import RequestException

def is_address_valid(address):
    base_url = "https://us-street.api.smartystreets.com/street-address"
    params = {
        'auth-id': '62e5a489-53d6-47b1-8eb4-2a7a84537fc3',
        'auth-token': '7zFKj3C0AnA4i30CDXMg',
        'street': address
    }

    try:
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            return len(data) > 0
        return False
    except RequestException:
        return False
