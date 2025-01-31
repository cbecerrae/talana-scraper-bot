from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from utils.shared import logger, send_keys, click
import time
import timeout_decorator

# Sets a timeout of 120 seconds (2 minutes) for the decorated function
@timeout_decorator.timeout(120, use_signals=False)
def login(ChromeDriver: WebDriver, email: str, password: str):
    """
    Automates the login process for the Talana platform.

    :param ChromeDriver: WebDriver instance used to interact with the web page.
    :param email: User's email address for login.
    :param password: User's password for login.
    """
    
    # Start the login process
    logger.info('Starting login process.')
    driver = ChromeDriver  # Get the Chrome driver
    
    talana_url = 'https://peru.talana.com/es/remuneraciones/'  # Talana URL
    logger.info('Navigating to the Talana login page.')
    driver.get(talana_url)  # Access the Talana URL
    logger.info('Successfully entered the Talana login page.')
    
    fill_user_input(driver, email)  # Call the function to enter the user email
    fill_password_input(driver, password)  # Call the function to enter the user password
    click_login_button(driver) # Call the function to enter the press the login button
    
    time.sleep(15) # Wait for the page to load
    logger.info('Login process finished successfully.')
    
def fill_user_input(driver: WebDriver, email: str):
    """
    Enters the user's email into the login input field.

    :param driver: WebDriver instance used to interact with the web page.
    :param email: User's email address to be entered.
    """
    
    # Enter the user email in the corresponding field
    logger.info('Entering the user email.')
    
    send_keys(driver, (By.CSS_SELECTOR, 'input[data-cy="talana-user-input"]'), email)  # Send the user email to the corresponding field
    
    logger.info('User email entered successfully.')

def fill_password_input(driver: WebDriver, password: str):
    """
    Enters the user's password into the login input field.

    :param driver: WebDriver instance used to interact with the web page.
    :param password: User's password to be entered.
    """
    
    # Enter the user password in the corresponding field
    logger.info('Entering the user password.')
    
    send_keys(driver, (By.CSS_SELECTOR, 'input[data-cy="talana-password-input"]'), password)  # Send the user password to the corresponding field
    
    logger.info('User password entered successfully.')

def click_login_button(driver: WebDriver):
    """
    Clicks the login button to submit the credentials.

    :param driver: WebDriver instance used to interact with the web page.
    """
    
    # Click the login button
    logger.info('Clicking the login button.')
    
    click(driver, (By.CSS_SELECTOR, 'button[data-cy="talana-login-button"]'))  # Click the login button
    
    logger.info('Login button clicked successfully.')