import requests
import json


class Pyelp:
    def __init__(self, key, timeout_s=None):
        """
        Instantiate Pyelp object with a given key
        :param key: API key from Yelp
        :param timeout_s: How long in seconds ...? TODO
        """

        self._key = key
        self._timeout = timeout_s
        self._session = requests.Session()
        self._headers = {
            'Authorization': f'Bearer {key}'
        }
        self._base_url = "https://api.yelp.com/v3/"

    def query_businesses(self, endpoint, **kwargs):
        if not endpoint:
            raise ValueError("Please provide a valid business extension.")
        query_url = self._base_url + "businesses/" + endpoint
        return self._query(query_url, **kwargs)

    def query_all_businesses(self, endpoint, **kwargs):
        response = self.query_businesses(endpoint, **kwargs)
        businesses = []
        businesses.extend(response['businesses'])
        start = 0
        total = response['total']
        limit = kwargs.get('limit', 50)

        while start != total:
            start += limit
            kwargs['offset'] = start
            response = self.query_businesses(endpoint, **kwargs)
            print(start, total, len(businesses))
            if 'error' in response:
                print("stopping")
                break
            else:
                print(response['businesses'][0]['id'])
                businesses.extend(response['businesses'])
        self.businesses = businesses
        return businesses

    def dump_to_json(self, filename="original"):
        with open(filename, 'w') as fout:
            json.dump(self.businesses, fout)

    @staticmethod
    def _clean_parameters(kwargs):
        """Remove all parameters that have None value
        TODO: expand this to check for types
        """
        return dict((k, v) for k, v in kwargs.items())

    def _query(self, url, **kwargs):
        """
        Make a query using given url, authorization headers, and parameters
        :param url: url to make a request from
        :param kwargs: parameters and extra
        :return: json response
        """
        parameters = self._clean_parameters(kwargs)
        response = self._session.get(url, headers=self._headers, params=parameters)

        return response.json()
