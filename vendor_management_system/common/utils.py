import logging
logger = logging.getLogger(__name__)


class CommonUtils:
    """
    Utility class containing common methods.

    Attributes:
        logger (Logger): The logger instance for logging messages.

    """
    @staticmethod
    def log(message):
        """
        Log a warning message using the logger.

        Parameters:
            message (str): The message to be logged.

        """
        logger.warning(message)