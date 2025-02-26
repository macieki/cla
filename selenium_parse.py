import csv
import logging
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium_helpers import find_and_click_elements  # Import the helper function if needed

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Input and output CSV file names
input_csv = "ads_data_unique.csv"
output_csv = "ads_data_with_details.csv"

# Read the initial data from CSV
data_rows = []
with open(input_csv, 'r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        data_rows.append(row)

def log_element_click(element):
    """Logs the clicked element's details."""
    try:
        logging.info(f"Clicked element with text: '{element.text}' and tag: <{element.tag_name}>")
    except Exception as e:
        logging.warning(f"Could not retrieve element details: {e}")

# Setup Selenium WebDriver (using Chrome here)
options = Options()
options.add_argument("--start-maximized")
# Uncomment the next line to run headless:
# options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

def scrape_by_testid(testid):
    """Helper to find an element by its data-testid attribute and return its text."""
    try:
        element = driver.find_element(By.CSS_SELECTOR, f"div[data-testid='{testid}']")
        return element.text.strip()
    except Exception:
        logging.info(f"Element with data-testid '{testid}' not found.")
        return ""

for i, row in enumerate(data_rows, start=1):
    link = row.get("link", "")
    if not link:
        logging.warning(f"Row {i}: No link found, skipping.")
        continue

    logging.info(f"Processing link {i}/{len(data_rows)}: {link}")
    try:
        driver.get(link)
    except Exception as e:
        logging.error(f"Error loading link: {link}. Error: {e}")
        continue

    # Wait for page to load
    time.sleep(10)

    # Accept cookies
    try:
        cookie_btn = driver.find_element(By.ID, "onetrust-accept-btn-handler")
        cookie_btn.click()
        logging.info("Clicked cookie accept button.")
    except Exception:
        logging.info("Cookie accept button not found or already accepted.")
    time.sleep(1)

    # Process accordions one-by-one using the new selector
    accordion_selector = "div[data-testid=collapsible-groups-wrapper] > div > div > header"
    try:
        accordions = driver.find_elements(By.CSS_SELECTOR, accordion_selector)
        accordion_count = len(accordions)
        logging.info(f"Found {accordion_count} accordion toggles.")
    except Exception as e:
        logging.error(f"Error finding accordion toggles: {e}")
        accordion_count = 0

    # Iterate over each accordion toggle individually
    for idx in range(accordion_count):
        try:
            # Re-locate toggles (DOM might change) and check index bounds
            accordions = driver.find_elements(By.CSS_SELECTOR, accordion_selector)
            if idx >= len(accordions):
                logging.info("No more accordion toggles available.")
                break
            accordion = accordions[idx]
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", accordion)
            time.sleep(0.5)
            accordion.click()
            logging.info(f"Clicked accordion toggle {idx+1}")
            time.sleep(1)  # Wait for accordion content to load

            # Now scrape the data-testid elements from the currently open accordion
            version_value        = scrape_by_testid('version')
            color_value          = scrape_by_testid('color')
            transmission_value   = scrape_by_testid('transmission')
            country_value        = scrape_by_testid('country_origin')
            original_owner_value = scrape_by_testid('original_owner')
            no_accident_value    = scrape_by_testid('no_accident')

            # Update row values if non-empty (if multiple accordions yield values, later ones overwrite earlier)
            if version_value:
                row["Version"] = version_value
            if color_value:
                row["Color"] = color_value
            if transmission_value:
                row["Transmission"] = transmission_value
            if country_value:
                row["Country"] = country_value
            if original_owner_value:
                row["Original_owner"] = original_owner_value
            if no_accident_value:
                row["No_accident"] = no_accident_value

        except Exception as e:
            logging.error(f"Error processing accordion toggle {idx+1}: {e}")

    # Now, scrape the "Najważniejsze" section for additional metadata
    try:
        h2_element = driver.find_element(By.XPATH, "//h2[contains(text(), 'Najważniejsze')]")
        sibling_div = h2_element.find_element(By.XPATH, "following-sibling::div[1]")
    except Exception as e:
        logging.error(f"Error finding 'Najważniejsze' section: {e}")
        sibling_div = None

    type_value = ""
    capacity_value = ""
    power_value = ""
    if sibling_div:
        try:
            type_elem = sibling_div.find_element(By.XPATH, ".//p[contains(text(), 'Typ nadwozia')]")
            type_value = type_elem.find_element(By.XPATH, "following-sibling::p[1]").text.strip()
        except Exception:
            logging.info("Typ nadwozia not found.")
        try:
            capacity_elem = sibling_div.find_element(By.XPATH, ".//p[contains(text(), 'Pojemność skokowa')]")
            capacity_value = capacity_elem.find_element(By.XPATH, "following-sibling::p[1]").text.strip()
        except Exception:
            logging.info("Pojemność skokowa not found.")
        try:
            power_elem = sibling_div.find_element(By.XPATH, ".//p[contains(text(), 'Moc')]")
            power_value = power_elem.find_element(By.XPATH, "following-sibling::p[1]").text.strip()
        except Exception:
            logging.info("Moc not found.")

    row["Type"]     = type_value
    row["Capacity"] = capacity_value
    row["Power"]    = power_value

driver.quit()

# Write the enriched data to a new CSV file
csv_columns = list(data_rows[0].keys())
try:
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in data_rows:
            writer.writerow(data)
    logging.info(f"Second round data extraction complete. {len(data_rows)} ads written to {output_csv}")
except Exception as e:
    logging.error(f"Error writing to CSV file: {e}")
