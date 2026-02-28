import sys
from networkSecurity.Logging.logger import logger

class NetworkSecurityException(Exception):
    """Base class for all exceptions in the network security module."""
    def __init__(self, error_message: str, error_details: str):
        self.error_message = error_message
        _, _, exc_tb = sys.exc_info()
        if exc_tb is not None:
            self.line_number = exc_tb.tb_lineno
            self.file_name = exc_tb.tb_frame.f_code.co_filename
        else:
            self.line_number = None
            self.file_name = None
    
    def __str__(self):
        location = f"file: {self.file_name} at line: {self.line_number}" if self.file_name and self.line_number else "unknown location"
        return f"Error occurred in {location} with message: {str(self.error_message)}"

if __name__ == "__main__":
    try:
        logger.info("Testing NetworkSecurityException")
        raise NetworkSecurityException("This is a test error message", "Additional error details")
    except NetworkSecurityException as e:
        print(e)