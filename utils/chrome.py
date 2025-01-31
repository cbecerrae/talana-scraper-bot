from selenium.webdriver import Chrome, ChromeOptions
import os

def get_driver():
    """
    Initializes and configures a Chrome WebDriver instance with specific options.

    The function sets various Chrome options to optimize performance, prevent 
    automation detection, and ensure compatibility with different environments.

    :return: An instance of the Chrome WebDriver with predefined configurations.
    """
    
    # Initializes the Chrome browser options
    options = ChromeOptions()

    # Prevents automation detection by websites
    options.add_argument('--disable-blink-features=AutomationControlled')

    # Runs the browser in headless mode (without a graphical interface)
    options.add_argument('--headless=new')

    # Launches the browser in maximized mode
    options.add_argument("--start-maximized")

    # Defines the window size to ensure all elements are visible
    options.add_argument('--window-size=1920,1080')

    # Reduces the verbosity of the browser logs to errors
    options.add_argument('--log-level=3')

    # Changes the user-agent to simulate a standard browser and avoid bot blocking
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36')

    # Configuration to avoid errors in non-sandboxed environments
    options.add_argument('--no-sandbox')

    # Reduces shared memory usage in the system (avoids certain errors on resource-limited systems)
    options.add_argument('--disable-dev-shm-usage')

    # Sets the default download directory to the current working directory
    options.add_experimental_option("prefs", {"download.default_directory": os.getcwd()})

    # Returns an instance of the Chrome driver with the configured options
    return Chrome(options=options)
