from common.custom_exceptions import CustomExceptions
from common.utils import CommonUtils
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


class AuthenticationHelper:
    """
    A helper class for user authentication tasks, including user login and registration.

    Methods:
        __init__(self):
            Initialize an instance of the AuthenticationHelper.

    """        
    def __init__(self):
        pass

    def login_user(self, data):
        """
        Authenticate a user based on provided email and password and generate access and refresh tokens.

        Parameters:
            data (dict): A dictionary containing user login data.
                Required keys: 'email', 'password'.

        Returns:
            dict: A dictionary containing access token, refresh token, and user details.
                Keys: 'access_token', 'refresh_token', 'user_details'.
                User details include 'username' and 'email'.

        Raises:
            CustomExceptions: If both email and password are not provided or if login credentials are invalid.

        """
        email = data.get('email', None).lower()
        password = data.get('password', None)

        if not email or not password:
            raise CustomExceptions('Both email and password are mandatory.')
        
        # Authenticating user.
        user_obj = authenticate(email=email, password=password)

        if not user_obj:
            raise CustomExceptions('Please provide valid login credentials.')
        user_details = {
            "username": user_obj.username,
            "email": user_obj.email
        }
        # Generating access and refresh tokens using simple-jwt.
        refresh_token = RefreshToken.for_user(user_obj)
        access_token = refresh_token.access_token

        response_object = {
            "access_token": str(access_token),
            "refresh_token": str(refresh_token),
            "user_details": user_details
        }

        return response_object

    def register_user(self, data):
        """
        Register a new user by creating a User object with the provided username, email, and password.

        Parameters:
            data (dict): A dictionary containing user registration data.
                Required keys: 'username', 'email', 'password'.

        Raises:
            CustomExceptions: If the user is already registered or if there is an unexpected error during registration.

        """
        username = data.get('username', None).lstrip()
        email = data.get('email', None).lower().lstrip()
        password = data.get('password', None).lstrip()
        try:
            user = User.objects.get(email=email)
            if user is not None:
                raise CustomExceptions('User already registered.')
        except User.DoesNotExist:
            # Registering a user.
            user_obj = User.objects.create(username=username, email=email, password=password)
            user_obj.set_password(password)
            user_obj.save()
        except Exception as e:
            CommonUtils.log(e)
            raise CustomExceptions(e)   