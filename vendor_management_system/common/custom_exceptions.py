class CustomExceptions(Exception):
    """
    Custom exception class for handling application-specific exceptions.

    This class extends the built-in Exception class and is used for raising custom exceptions
    with a specific error message.

    Attributes:
        msg (str): The error message associated with the exception.

    Methods:
        __init__(self, msg: str): Initialize the CustomExceptions instance with the given error message.
    """

    def __init__(self, msg):
        """
        Initialize the CustomExceptions instance with the given error message.

        Parameters:
            msg (str): The error message associated with the exception.
        """
        super().__init__(msg)


class CustomExceptionsDict(CustomExceptions):
    """
    Custom exception class for handling application-specific exceptions with additional result dictionary.

    This class extends the CustomExceptions class and includes an additional result dictionary
    for providing detailed error information.

    Attributes:
        error_message (str): The error message associated with the exception.
        result_dict (dict): Additional result dictionary for detailed error information.

    Methods:
        __init__(self, error_message: str, result_dict: dict): Initialize the CustomExceptionsDict instance
            with the given error message and result dictionary.
        get_error_msg(self) -> str: Get the error message associated with the exception.
        get_result_dict(self) -> dict: Get the result dictionary associated with the exception.
    """
    def __init__(self, error_message, result_dict):
        """
        Initialize the CustomExceptionsDict instance with the given error message and result dictionary.

        Parameters:
            error_message (str): The error message associated with the exception.
            result_dict (dict): Additional result dictionary for detailed error information.
        """
        super().__init__(error_message)
        self.error_message = error_message
        self.result_dict = result_dict

    def get_error_msg(self):
        """
        Get the error message associated with the exception.

        Returns:
            str: The error message.
        """
        return self.error_message

    def get_result_dict(self):
        """
        Get the result dictionary associated with the exception.

        Returns:
            dict: The result dictionary.
        """
        return self.result_dict


class CustomFormErrorExceptions(CustomExceptionsDict):
    """
    Custom exception class for handling form-related errors with additional result dictionary and error list.

    This class extends the CustomExceptionsDict class and includes an additional error list
    for handling form-related errors and providing detailed error information.

    Attributes:
        error_message (str): The error message associated with the exception.
        result_dict (dict): Additional result dictionary for detailed error information.
        error_list (list): List of form-related errors.

    Methods:
        __init__(self, error_message: str, result_dict: dict, error_list: list=[]): Initialize the
            CustomFormErrorExceptions instance with the given error message, result dictionary, and error list.
        get_error_list(self) -> list: Get the list of form-related errors.
        get_error_msg(self) -> str: Get the error message associated with the exception.
        get_full_error_dict(self) -> dict: Get a dictionary containing both error list and result dictionary.
    """
    def __init__(self, error_message, result_dict, error_list=[]):
        """
        Initialize the CustomFormErrorExceptions instance with the given error message, result dictionary, and error list.

        Parameters:
            error_message (str): The error message associated with the exception.
            result_dict (dict): Additional result dictionary for detailed error information.
            error_list (list, optional): List of form-related errors. Defaults to an empty list.
        """
        super().__init__(error_message, result_dict)
        self.error_messaage = error_message
        self.error_list = error_list

    def get_error_list(self):
        """
        Get the list of form-related errors.

        Returns:
            list: List of form-related errors.
        """
        return self.error_list

    def get_error_msg(self):
        """
        Get the error message associated with the exception.

        Returns:
            str: The error message.
        """
        return self.error_messaage

    def get_full_error_dict(self):
        """
        Get a dictionary containing both error list and result dictionary.

        Returns:
            dict: Dictionary containing "error_list" and "error_details".
        """
        error_dict =  {"error_list": self.get_error_list(), "error_details": self.get_result_dict()}
        return error_dict    