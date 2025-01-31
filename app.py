from argparse import ArgumentParser
from utils.chrome import get_driver
from utils.login import login
from utils.mark_attendance import mark_attendance
from utils.shared import logger, take_screenshot, send_sns_notification
import sys
import time

def main():
    """
    Main function that handles the execution of the attendance marking process.

    This function parses command-line arguments, initializes the Chrome WebDriver, 
    performs user authentication, and marks attendance based on the specified type 
    ('In' or 'Out'). 

    If an exception occurs during execution, it logs the error, captures a screenshot 
    for debugging, sends an SNS notification, and exits with a non-zero status.

    Command-line arguments:
    --type      : Specifies the attendance type ('In' for check-in, 'Out' for check-out).
    --email     : Specifies the user email for login authentication.
    --password  : Specifies the user password for login authentication.
    """
    
    # ArgumentParser is used to handle command line arguments
    parameters = ArgumentParser()

    # Required arguments: type, email, and password
    parameters.add_argument('--type', required=True, choices=['In', 'Out'], help="Specifies whether the attendance mark is 'In' or 'Out'.")
    parameters.add_argument('--email', required=True, help="Specifies the user email.")
    parameters.add_argument('--password', required=True, help="Specifies the user password.")
    
    # Parse the arguments provided by the user
    arguments = parameters.parse_args()

    # Initialize the ChromeDriver instance
    ChromeDriver = get_driver()
    
    try:
        # Execute the login and mark attendance functions
        login(ChromeDriver, arguments.email, arguments.password)
        mark_attendance(ChromeDriver, arguments.type)
        
    except Exception as e:
        # Log the error message and the traceback if an exception occurs
        logger.error(f'Exception caught: {str(e)}')
        logger.exception('Detailed traceback:')
        
        # Take a screenshot for debugging purposes
        screenshot_path = take_screenshot(ChromeDriver)
        
        # Send SNS notification
        send_sns_notification(str(e), screenshot_path)
        
        # Exit the script with a non-zero status to indicate that an error occurred
        sys.exit(1)

if __name__ == '__main__':
    main()
