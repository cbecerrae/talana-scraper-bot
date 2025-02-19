from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import boto3
import logging
import os
import time

# Get environment variables (raises KeyError if missing)
SNS_TOPIC_ARN = os.environ['SNS_TOPIC_ARN']
S3_BUCKET_NAME = os.environ['S3_BUCKET_NAME']
AWS_REGION = os.environ['AWS_REGION']

def send_keys(driver: WebDriver, locator, keys: str):
    """
    Waits until the specified element is clickable and then sends the given text input.

    :param driver: WebDriver instance used to interact with the web page.
    :param locator: Tuple (By.<METHOD>, value) used to locate the element.
    :param keys: The text to be sent to the located element.
    """
    
    # Wait until the element is clickable, then send the values
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable(locator))
    time.sleep(2)  # Wait an additional 2 seconds before sending the values
    driver.find_element(*locator).send_keys(keys)  # Send the values to the located element

def click(driver: WebDriver, locator):
    """
    Waits until the specified element is clickable and then performs a click action.

    :param driver: WebDriver instance used to interact with the web page.
    :param locator: Tuple (By.<METHOD>, value) used to locate the element.
    """
    
    # Wait until the element is clickable, then click
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable(locator))
    driver.find_element(*locator).click()  # Click on the element

def get_logger():
    """
    Configures and returns a logger instance with a specific log format.

    :return: Configured logger instance with INFO level and a formatted output.
    """
    
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)  # Set the logging level to INFO
    formatter = logging.Formatter('[%(levelname)s] %(message)s')  # Define the log message format
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.handlers = [handler]
    
    return logger

logger = get_logger()  # Initialize the logger

def take_screenshot(driver: WebDriver):
    """
    Captures a full-page screenshot using Selenium, saves it locally with a timestamp,  
    uploads it to an S3 bucket, and returns the S3 URI.

    :param driver: WebDriver instance used to interact with the web page.
    :return: S3 URI of the uploaded screenshot.
    :raises: Logs an error message if the screenshot capture or upload fails.
    """

    # Captures a full-page screenshot
    try:
        # Get the full width and height of the web page
        width = driver.execute_script('return document.body.scrollWidth')
        height = driver.execute_script('return document.body.scrollHeight')
        driver.set_window_size(width, height)  # Resize the window to fit the full page
        
        # Generate a timestamp for the filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'{timestamp}.png'  # Define the filename with the timestamp
        
        # Take and save the screenshot
        full_body_element = driver.find_element(By.TAG_NAME, 'body')
        full_body_element.screenshot(filename)
        logger.info(f'Screenshot taken and saved as {filename}.')
        
        # Define the S3 path
        s3_bucket = S3_BUCKET_NAME
        s3_path = f'errors/screenshots/{filename}'
        s3_uri = f's3://{s3_bucket}/{s3_path}'
        
        # Upload the screenshot to S3
        s3 = boto3.client('s3')
        s3.upload_file(filename, s3_bucket, s3_path, ExtraArgs={'ContentType': 'image/png'})
        logger.info(f'New screenshot uploaded: {s3_uri}')
        
        # Return the S3 URI of the screenshot
        return s3_uri
    except Exception as e:
        # Log an error message if taking the screenshot fails
        logger.error(f'Error while taking screenshot.')
        logger.error(f'Exception caught: {str(e)}')

def send_sns_notification(error: str, screenshot_s3_uri: str = None):
    """
    Sends an SNS notification with error details and an optional screenshot URL.
    
    :param error: Description of the error.
    :param screenshot_s3_uri: (Optional) S3 URI of the screenshot.
    """
    
    # Construct the error message with more details
    message = f"An error occurred during the Talana Automated Attendance Marking process.\n\n"
    message += f"Error Details: {error}\n"
    
    # If a screenshot is available, include its link in the message
    if screenshot_s3_uri:
        message += f"\nA screenshot of the issue has been uploaded to S3:\n{screenshot_s3_uri}\n"
    
    logger.info("Sending SNS notification...")
    
    # Initialize the SNS client
    sns = boto3.client('sns', region_name=AWS_REGION)
    
    # Retrieve the SNS topic ARN from environment variables
    topic_arn = os.getenv('SNS_TOPIC_ARN')
    
    # Publish the message to the SNS topic
    sns.publish(
        TopicArn=topic_arn,
        Message=message,
        Subject='[ERROR] Talana Automated Attendance Marking Notification'
    )
    
    logger.info('SNS notification sent successfully.')