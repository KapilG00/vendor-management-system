from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response


class ResultBuilder:
    """
    Builder class for constructing standardized API response.

    This class provides methods to set the status, message, and result object for an API response.
    The `get_response_rest` method constructs and returns a Response object with the specified details.

    Attributes:
        RESPONSE_STATUS_OK (str): Constant representing the 'OK' status type.

    Methods:
        success(): Set the status to success.
        fail(): Set the status to failure.
        message(status_message: str): Set the status message.
        result_object(result: dict): Set the result object.
        get_response_rest() -> Response: Construct and return a standardized Response object.
    """
    
    RESPONSE_STATUS_OK = "RESPONSE_STATUS_OK"

    def __init__(self):
        """
        Initialize the ResultBuilder with default values.
        """
        self.results = {}
        self.status_code = 1
        self.status_type = self.RESPONSE_STATUS_OK
        self.status_message = ""
        self.status = status.HTTP_200_OK

    def success(self):
        """
        Set the status to success.

        Returns:
            ResultBuilder: The ResultBuilder instance for method chaining.
        """
        self.status_code = 1
        return self

    def fail(self):
        """
        Set the status to failure.

        Returns:
            ResultBuilder: The ResultBuilder instance for method chaining.
        """
        self.status_code = -1
        return self

    def message(self, status_message):
        """
        Set the status message.

        Parameters:
            status_message (str): The status message to be set.

        Returns:
            ResultBuilder: The ResultBuilder instance for method chaining.
        """
        self.status_message = status_message
        return self

    def result_object(self, result):
        """
        Set the result object.

        Parameters:
            result (dict): The result object to be set.

        Returns:
            ResultBuilder: The ResultBuilder instance for method chaining.
        """
        self.results = result
        return self
    
    def get_response_rest(self):
        """
        Construct and return a standardized Response object.

        Returns:
            Response: The standardized API response.

        """
        content = {}
        content['status_code'] = self.status_code
        content['status_type'] = self.status_type
        content['status_message'] = self.status_message
        content['results'] = self.results
        response = Response(content, status=self.status)
        response.accepted_renderer = JSONRenderer()
        response.accepted_media_type = "application/json"
        response.renderer_context = {}

        return response