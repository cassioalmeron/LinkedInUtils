import time
import logging
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # This ensures logs go to console
    ]
)
logger = logging.getLogger(__name__)

def get_driver():
    chrome_driver_path = os.getenv('CHROME_DRIVER_PATH')
    
    options = webdriver.ChromeOptions()
    if chrome_driver_path:
        options.binary_location = chrome_driver_path
    
        # Add necessary options for server environment
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--user-data-dir=/tmp/chrome-user-data")
        options.add_argument("--remote-debugging-port=9222")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-plugins")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-web-security")
        options.add_argument("--allow-running-insecure-content")
    
    return webdriver.Chrome(options=options)

def get_content(url:str) -> str:
    try:
        driver = get_driver()
        
        try:
            logger.info(f"Navigating to LinkedIn post: {url}")
            driver.get(url)
            
            try:
                content_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "break-words"))
                )
                
                content = content_element.text
                logger.info(f"Content found, length: {len(content)} characters")
                
                return content
                
            except (TimeoutException, NoSuchElementException) as e:
                error_msg = f"Content not found on page: {str(e)}"
                logger.error(error_msg)
                raise Exception(error_msg)
            
        except WebDriverException as e:
            error_msg = f"WebDriver error: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)
            
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        logger.error(error_msg)
        raise Exception(error_msg)

    finally:
        try:
            driver.quit()
        except:
            pass
        
if __name__ == "__main__":
    content = get_content("https://www.linkedin.com/posts/pedro-cons_hot-to-build-your-first-ai-net-app-in-under-activity-7373672066266361856-PsyG/?utm_source=share&utm_medium=member_desktop&rcm=ACoAAC5vLqwBf23HT7dx1ufe2wEyogCDZvdPkB4")
    print(content)