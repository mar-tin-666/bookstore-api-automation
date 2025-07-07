"""
CommonAPI class for API clients.
This class provides a base implementation for API clients, including common functionality such as
creating base URLs and handling default headers.
"""

class CommonAPI: # pylint: disable=too-few-public-methods
    """
    Base class for API clients.
    This class provides a base implementation for API clients, including common functionality
    such as creating base URLs and handling default headers.
    """
    def __init__(self):
        """
        Initializes the CommonAPI instance with default settings.
        """
        self.hostname = "https://fakerestapi.azurewebsites.net/"
        self.timeout = 10  # seconds
        self.default_headers = {"Content-Type": "application/json"}

    def _create_base_url(self, api_path=""):
        """
        Create the base URL for the API.
        Args:
            api_path (str): The API path to append to the hostname.
        Returns:
            str: The complete base URL for the API.
        """
        return self.hostname + api_path
