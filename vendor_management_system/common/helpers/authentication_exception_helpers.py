from rest_framework.views import exception_handler
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework.response import Response


def token_exception_handler(exc, context):
    """
    Custom exception handler for handling token-related exceptions.

    This function intercepts exceptions related to token validation, such as TokenError and InvalidToken,
    and returns a customized response with appropriate status and message.

    Parameters:
        exc (Exception): The exception instance.
        context (dict): The context of the exception.

    Returns:
        Response: A customized response with details about the token-related exception.

    """
    response = exception_handler(exc, context)

    if isinstance(exc, (TokenError, InvalidToken)):
        custom_data = {
            "status_code": -1,
            "status_type": "RESPONSE_STATUS_UNAUTHORIZED",
            "status_message": "Token is invalid or expired",
            "results": {}
        }
        if response is not None:
            response.data = custom_data
        else:
            response = Response(custom_data, status=401)

    return response
