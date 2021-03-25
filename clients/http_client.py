import requests


class HTTPClient:
    """
    HTTP client for jobs.tut.by
    """

    @staticmethod
    def get(url, params=None, **kwargs):
        """
        Returns response for http-request get
        """
        return requests.get(url, params, **kwargs)

    @staticmethod
    def post(url, params=None, json=None, **kwargs):
        """
        Returns response for http-request post
        """
        return requests.post(url, params, json, **kwargs)

    @staticmethod
    def delete(url, **kwargs):
        """
        Returns response for http-request delete
        """
        return requests.delete(url, **kwargs)
