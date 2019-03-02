import requests

class Request:
    ''' Class containings wrapper functions around request library '''
    def get(param):
        ''' Wrapper around GET request '''
        ''' Parameters: path parameter '''
        ''' Return value: raw json if valid, -1 if error '''
        response = requests.get('http://cec2019.ca/' + param, headers = {'token': \
            'toronto-gWbRmC3Vo7MKnd2niVuBoh76xPxaT8B3noPVnmwanr885uuZf68MEfzuPhRVJFBY'})

        json = response.json()
        if json["type"] == "ERROR":
            return -1

        return json

    def post(param, options=''):
        ''' Wrapper around POST request '''
        ''' Parameters: path parameter, option '''
        ''' Return value: raw json if valid, -1 if error '''
        response = requests.post('http://cec2019.ca/' + param + '/' + options, headers = {'token': \
            'toronto-gWbRmC3Vo7MKnd2niVuBoh76xPxaT8B3noPVnmwanr885uuZf68MEfzuPhRVJFBY'})

        json = response.json()
        if json["type"] == "ERROR":
            return -1

        return json
