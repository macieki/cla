import os
import csv
import logging
from bs4 import BeautifulSoup

# Configure logging to show debug messages.
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

# List of HTML files in the root folder
html_files = ['1.htm', '2.htm', '3.htm', '4.htm', '5.htm', '6.htm', '7.htm', '8.htm', '9.htm', '10.htm',  '11.htm', '12.htm', '13.htm', '14.htm', '15.htm', '16.htm', '17.htm']

# List to hold extracted ad data
data_list = []

for file_name in html_files:
    if not os.path.exists(file_name):
        logging.warning(f"File {file_name} does not exist. Skipping...")
        continue

    logging.info(f"Processing file: {file_name}")
    with open(file_name, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Log a snippet of the file content for debugging

    soup = BeautifulSoup(html_content, 'lxml')
    # Use the selector: article > section as the main container for each ad.
    sections = soup.select('article > section')
    logging.debug(f"Found {len(sections)} ad sections in {file_name}")

    for idx, section in enumerate(sections, start=1):
        # --- Extract Title and Link ---
        # Assume the first <h2> with an <a> tag holds the title and link.
        h2 = section.find('h2')
        a_tag = h2.find('a') if h2 else None
        title = a_tag.get_text(strip=True) if a_tag else ''
        link = a_tag.get('href', '') if a_tag else ''

        # --- Extract Price ---
        # Look for the first <h3> inside the section for the price.
        h3 = section.find('h3')
        price = h3.get_text(strip=True) if h3 else ''
        logging.debug(f"Section {idx}: price='{price}'")

        # --- Extract Details (Mileage, Fuel Type, Transmission, Year) ---
        details = {}
        dl = section.find('dl')
        if dl:
            # Loop through each <dt> element and its corresponding <dd>
            for dt in dl.find_all('dt'):
                label = dt.get_text(strip=True).lower()  # Normalize label to lowercase
                dd = dt.find_next_sibling('dd')
                if dd:
                    details[label] = dd.get_text(strip=True)
        else:
            logging.debug(f"Section {idx}: No <dl> element found for details.")

        mileage = details.get('przebieg', '')
        fuel_type = details.get('rodzaj paliwa', '')
        gearbox = details.get('skrzynia biegów', '')
        year = details.get('rok produkcji', '')

        # --- Determine if the Seller is Private ---
        # Check if any <p> element in the section contains "1-wł"
        is_private = any("1-wł" in p.get_text() for p in section.find_all('p'))

        # Append the extracted data for this ad
        data_list.append({
            'link': link,
            'price': price,
            'year': year,
            'mileage': mileage,
            'title': title,
            'fuel_type': fuel_type,
            'gearbox': gearbox,
            'isPrivateSeller': is_private
        })

if not data_list:
    logging.error("No ad data was extracted. Check your HTML structure and selectors.")
else:
    logging.info(f"Extracted data for {len(data_list)} ads.")

# --- Write the Extracted Data to a CSV File ---
csv_columns = ['link', 'price', 'year', 'mileage', 'title', 'fuel_type', 'gearbox', 'isPrivateSeller']
csv_file = "ads_data.csv"

try:
    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in data_list:
            writer.writerow(data)
    logging.info(f"Data extraction complete. {len(data_list)} ads written to {csv_file}")
except Exception as e:
    logging.error(f"Error writing to CSV file: {e}")
