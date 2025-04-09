from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from utils.shared import logger, click
import time
import timeout_decorator

# Sets a timeout of 120 seconds (2 minutes) for the decorated function
@timeout_decorator.timeout(120, use_signals=False)
def mark_attendance(driver: WebDriver, mark_type: str):
    """
    Automates the attendance marking process by clicking the necessary elements.

    :param driver: WebDriver instance used to interact with the web page.
    :param mark_type: Type of attendance mark to select ('In' for entry, 'Out' for exit).
    """
    
    click_mark_attendance(driver)
    click_mark_type_selector(driver, mark_type)
    finish_mark_attendance(driver)
    
    time.sleep(15) # Wait for the page to load
    logger.info('Mark attendance process finished successfully.')

def click_mark_attendance(driver: WebDriver):
    """
    Clicks the button to start the attendance marking process.

    :param driver: WebDriver instance used to interact with the web page.
    """
    
    # Click the mark attendance button
    logger.info('Clicking the mark attendance button.')
    
    click(driver, (By.XPATH, '//button[@data-cy="pdt-mark-attendance"]'))  # Click the mark attendance button
    
    logger.info('Mark attendance button clicked successfully.')
    
def click_mark_type_selector(driver: WebDriver, mark: str):
    """
    Selects the specified attendance mark type from the available options.

    :param driver: WebDriver instance used to interact with the web page.
    :param mark: Type of attendance mark to select ('In' for entry, 'Out' for exit).
    """
    
    # Click the mark type selector and select the specified mark type
    logger.info(f'Entering the mark type "{mark}".')
    
    click(driver, (By.XPATH, '//input[@placeholder="Marca"]'))  # Click the mark type selector
    
    if mark == 'In':
        click(driver, (By.XPATH, '//span[text()="Entrada"]'))  # Select the "In" mark type
    elif mark == 'Out':
        click(driver, (By.XPATH, '//span[text()="Salida"]'))  # Select the "Out" mark type
    
    logger.info(f'Mark type "{mark}" entered successfully.')
    
def finish_mark_attendance(driver: WebDriver):
    """
    Clicks the button to complete the attendance marking process.

    :param driver: WebDriver instance used to interact with the web page.
    """
    
    # Click the finish mark button
    logger.info('Clicking the finish mark button.')
    
    click(driver, (By.XPATH, '//button[@data-cy="pdt-mark-confirmMarkAttendance"]'))  # Click the finish mark button
    
    logger.info('Finish mark button clicked successfully.')