import requests


class HTTPClient:
    """
    HTPP client for jobs.tut.by
    """

    @staticmethod
    def get(url, params=None, **kwargs):
        return requests.get(url, params, **kwargs)

    @staticmethod
    def post(url, params=None, json=None, **kwargs):
        return requests.post(url, params, json, **kwargs)

    @staticmethod
    def delete(url, **kwargs):
        return requests.delete(url, **kwargs)
