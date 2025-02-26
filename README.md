# Ads Data Scraper

This repository contains Python scripts that perform a multi-step process to scrape and enrich advertisement data. The process is divided into three main parts:

1. **HTML Data Extraction:**   Extract basic ad details (e.g., link, title, price, mileage, fuel type, gearbox, year, seller type) from local HTML files using BeautifulSoup.

2. **Selenium Data Enrichment:**   Open each ad link from the CSV generated in Part 1, interact with the page (e.g., accept cookies, expand accordions), and scrape additional metadata using Selenium. The enriched data is saved to a new CSV file.

3. **CSV Deduplication:**   Remove duplicate rows based on the `'link'` column so that each ad appears only once.

## Repository Structure

```
├── html_files/                # Folder containing input HTML files (e.g., 1.html, 2.html, etc.)
├── ads_data.csv               # Output from Part 1 (HTML Data Extraction)
├── ads_data_with_details.csv  # Output from Part 2 (Selenium Data Enrichment)
├── ads_data_unique.csv        # Output from Part 3 (Deduplicated CSV)
├── selenium_helpers.py        # Helper functions for Selenium interactions
├── selenium_parse.py          # Selenium script for data enrichment (Part 2)
├── dedupe_csv.py              # Script to remove duplicate rows based on 'link' (Part 3)
└── README.md                  # This file
```

## Prerequisites

- **Python 3.x**
- **pip** (Python package manager)
- **Required Python Packages:**
  - `beautifulsoup4`
  - `lxml`
  - `selenium`
- **WebDriver:**  Install a WebDriver (e.g., ChromeDriver) that is compatible with your browser version and ensure it is in your system's PATH.

Install the required packages using:

```bash
pip install beautifulsoup4 lxml selenium
```

## Usage

### 1. HTML Data Extraction

Run the script that parses the HTML files and extracts basic ad data into a CSV file (`ads_data.csv`):

```bash
python html_scraper.py
```

*Note: Ensure your HTML files are located in the correct directory and that the selectors in the script match the HTML structure.*

### 2. Selenium Data Enrichment

Run the Selenium script to open each ad link, interact with the page (accept cookies, expand accordions, etc.), and scrape additional metadata. This enriched data is saved to `ads_data_with_details.csv`:

```bash
python selenium_parse.py
```

*Notes:*

- The script scrolls and clicks each accordion one-by-one.
- The new accordion selector used is:  `div[data-testid=collapsible-groups-wrapper] > div > div > header`
- Make sure the WebDriver is installed and that the selectors match the target website.

### 3. CSV Deduplication

Run the deduplication script to remove duplicate rows from the CSV based on the `'link'` column. The result is saved as `ads_data_unique.csv`:

```bash
python dedupe_csv.py
```

This ensures that each ad link appears only once in the final CSV.

## Customization

- **HTML Selectors:**  Modify the BeautifulSoup selectors in `html_scraper.py` if the input HTML structure changes.

- **Selenium Selectors and Timing:**  Adjust XPath/CSS selectors and `time.sleep()` values in `selenium_parse.py` as needed for your target website and network conditions.

- **Deduplication Logic:**  The deduplication script currently filters out rows with duplicate `'link'` values. Adjust the logic if needed.

## Troubleshooting

- **Invalid URL Errors:**  Ensure valid URLs are passed to Selenium's `driver.get()`.

- **Empty CSV Files:**  Check that your input HTML files contain the expected structure and that selectors are correctly defined.

- **WebDriver Issues:**  Verify that the installed WebDriver is compatible with your browser version.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Selenium Documentation](https://selenium-python.readthedocs.io/)
