from rest_framework.views import APIView
from .helpers.authentication_helpers import AuthenticationHelper
from common.helpers.rest_api_helpers import ResultBuilder
from common.custom_exceptions import CustomExceptions, CustomFormErrorExceptions


class UserLoginView(APIView):
    """
    A class representing an API view for user login.

    This view allows users to log in and obtain authentication tokens.
    Simple-JWT authentication is used to secure endpoints.

    Methods:
        post(self, request, *args, **kwargs):
            Post method to login a user.
    """
    def post(self, request, *args, **kwargs):
        """
        Handle POST requests to authenticate a user and generate tokens for login.

        Parameters:
            request (HttpRequest): The HTTP request object.
            *args: Variable-length argument list.
            **kwargs: Not used.

        Request Data:
            - user_data (dict): A dictionary containing a user login information.        

        Returns:
            Response: A JSON response with the result of the login operation.
            Possible status codes:
                - 200 OK: Login successful, with authentication tokens.
                - 400 Bad Request: Invalid request data or user credentials.
                - 500 Internal Server Error: An unexpected error occurred.

        Raises:
            CustomFormErrorExceptions: If there is an issue with the request data format.
            CustomExceptions: For other custom exceptions.

        Request Data Format:
            {
                "email": "test@example.com",
                "password": "examplepassword"
            }

        Response Format:
            {
                "status_code": 1,
                "status_type": "RESPONSE_STATUS_OK",
                "status_message": "Login Successful.",
                "results": {
                    "access_token": "example_access_token",
                    "refresh_token": "example_refresh_token",
                    "user_details": {
                        "username": "test",
                        "email": "test@example.com"
                    }
                }
            }

        """
        user_data = request.data
        try:
            temp_resp = AuthenticationHelper().login_user(user_data)
            response_object = ResultBuilder().success().message("Login Successful.").result_object(temp_resp).get_response_rest()
        except CustomFormErrorExceptions as e:
            get_error_msg = e.get_error_msg()
            full_error_dict = e.get_full_error_dict()
            response_object = ResultBuilder().fail().message(get_error_msg).result_object(full_error_dict).get_response_rest()
        except CustomExceptions as e:
            err_msg = str(e)
            response_object = ResultBuilder().fail().message(err_msg).get_response_rest()
        except Exception as e:
            err_msg = str(e)
            response_object = ResultBuilder().fail().message(err_msg).get_response_rest()

        return response_object    
                 

class UserRegistrationView(APIView):
    """
    A class representing an API view for user registration.

    This view allows users to register and create a new account.

    Methods:
        post(self, request, *args, **kwargs):
            Post method to register a new user.
    """
    def post(self, request, *args, **kwargs):
        """
        Handle POST requests to register a new user.

        Parameters:
            request (HttpRequest): The HTTP request object.
            *args: Variable-length argument list.
            **kwargs: Not used.

        Request Data:
            - user_data (dict): A dictionary containing the new user information.        

        Returns:
            Response: A JSON response with the result of the registration operation.
            Possible status codes:
                - 201 Created: Registration successful, with user details.
                - 400 Bad Request: Invalid request data or user already exists.
                - 500 Internal Server Error: An unexpected error occurred.

        Raises:
            CustomFormErrorExceptions: If there is an issue with the request data format.
            CustomExceptions: For other custom exceptions.

        Request Data Format:
            {
                "username": "test",
                "password": "examplepassword",
                "email": "test@example.com"
            }

        Response Format:
            {
                "status_code": 1,
                "status_type": "RESPONSE_STATUS_OK",
                "status_message": "Registration Successful.",
                "results": null
            }

        """
        user_data = request.data
        try:
            temp_resp = AuthenticationHelper().register_user(user_data)
            response_object = ResultBuilder().success().message("Registration Successful.").result_object(temp_resp).get_response_rest()
        except CustomFormErrorExceptions as e:
            get_error_msg = e.get_error_msg()
            full_error_dict = e.get_full_error_dict()
            response_object = ResultBuilder().fail().message(get_error_msg).result_object(full_error_dict).get_response_rest()
        except CustomExceptions as e:
            err_msg = str(e)
            response_object = ResultBuilder().fail().message(err_msg).get_response_rest()
        except Exception as e:
            err_msg = str(e)
            response_object = ResultBuilder().fail().message(err_msg).get_response_rest()

        return response_object    