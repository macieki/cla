from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException, StaleElementReferenceException
import time

def find_and_click_elements(driver, by, selector, scroll_behavior='center', callback=None):
    """
    Finds elements by a given selector, scrolls to each, and clicks them.
    Retries if elements are intercepted or become stale.
    
    :param driver: Selenium WebDriver instance
    :param by: Locator strategy (By.ID, By.XPATH, By.CSS_SELECTOR, etc.)
    :param selector: The selector string for locating elements
    :param scroll_behavior: Defines scrolling position ('center', 'start', or 'end')
    :param callback: Optional function to execute after clicking an element
    """
    try:
        elements = driver.find_elements(by, selector)
        if not elements:
            print(f"No elements found for selector: {selector}")
            return False

        for element in elements:
            try:
                # Scroll to the element
                driver.execute_script(
                    "arguments[0].scrollIntoView({behavior: 'smooth', block: arguments[1]});", 
                    element, 
                    scroll_behavior
                )
                time.sleep(0.5)  # Small delay to ensure the element is in view

                # Click the element, retrying if needed
                attempts = 3
                while attempts > 0:
                    try:
                        element.click()
                        print(f"Clicked element: {selector}")
                        
                        # Execute callback if provided
                        if callback:
                            callback(element)
                        
                        break
                    except ElementClickInterceptedException:
                        print("Element click intercepted, retrying...")
                        time.sleep(1)
                    except StaleElementReferenceException:
                        print("Element went stale, retrying lookup...")
                        element = driver.find_element(by, selector)
                    attempts -= 1
            
            except Exception as e:
                print(f"Error clicking element {selector}: {e}")
        
        return True
    
    except NoSuchElementException:
        print(f"No elements found for selector: {selector}")
        return False

# Example usage: Uncomment and modify the URL and selector if you wish to test this module directly.
if __name__ == "__main__":
    driver = webdriver.Chrome()
    # Replace with a valid URL before testing.
    driver.get("https://example.com")
    find_and_click_elements(driver, By.CSS_SELECTOR, "your_css_selector")
