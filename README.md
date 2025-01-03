# Naver Finance Data Crawling Script

## Overview

This script crawls financial data from the **Naver Finance** website, specifically extracting key financial metrics such as **Operating Profit**, **Total Assets**, and **Sales**. The data is then saved into a **CSV file** for further analysis. The script uses **Selenium** to automate browser interaction and **Pandas** to extract and save the data.

## Requirements

To run this script, the following software and libraries are required:

- **Python 3.x**
- **Chrome Browser** (Make sure ChromeDriver is installed on your system)
- **Selenium**: For browser automation
- **Pandas**: For data processing and saving

### Installing Dependencies

1. Install the required libraries:

    ```bash
    pip install selenium pandas
    ```

2. **Install ChromeDriver**:
   - Download the appropriate **ChromeDriver** based on your Chrome browser version.
   - [Download ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/)
   - Ensure ChromeDriver is added to your system PATH or specify the path in the script.

## How to Use

1. **Download the script**:
   - Clone or download this script to your local machine.

2. **Run the script**:
   - To run the script, use the following command:

    ```bash
    python scrape_naver_finance.py
    ```

3. **Check the results**:
   - After running the script, a file named `fin.csv` will be created in your working directory. This file contains the crawled financial data from Naver Finance.
   - The file is saved in **UTF-8** encoding.

## How It Works

1. **Open and Maximize Browser**:
   - The script creates a **Chrome** browser instance using `webdriver.Chrome()` and maximizes the window using `maximize_window()`.

2. **Navigate to Naver Finance**:
   - The script navigates to the URL `https://finance.naver.com/sise/sise_market_sum.naver?&page=` and dynamically loads the pages to crawl data.

3. **Clear Selected Fields and Select Specific Items**:
   - It first unchecks any previously selected fields and then selects the desired financial metrics (Operating Profit, Total Assets, and Sales) by interacting with the checkboxes on the webpage.

4. **Extract Data**:
   - The script uses **Pandas** (`read_html()`) to extract table data from the HTML of the page.
   - It cleans the data by removing rows and columns with all missing values using `dropna()`.

5. **Save Data**:
   - The extracted data is saved in a **CSV file** named `fin.csv`. If the file already exists, the data is appended without headers; otherwise, it is written with headers.

6. **Close the Browser**:
   - After completing the crawl for all pages, the script closes the browser using `browser.quit()`.

## Notes

- This script crawls data from the **Market Summary** page of Naver Finance. If the structure of the page changes, the script may not work correctly.
- If you wish to select other financial metrics, you can add them to the `items_to_select` list.
- The script will automatically stop if no data is found on a page.

## Example Code

```python
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import os

# Create and maximize the browser window
browser = webdriver.Chrome()
browser.maximize_window()

# Navigate to the URL
url = 'https://finance.naver.com/sise/sise_market_sum.naver?&page='
browser.get(url)

# Uncheck any already selected fields
checkboxes = browser.find_elements(By.NAME, 'fieldIds')
for checkbox in checkboxes:
    if checkbox.is_selected():
        checkbox.click()

# Select the desired financial metrics (Operating Profit, Total Assets, Sales)
items_to_select = ['영업이익', '자산총계', '매출액']
for checkbox in checkboxes:
    parent = checkbox.find_element(By.XPATH, '..')
    label = parent.find_element(By.TAG_NAME, 'label')
    if label.text in items_to_select:
        checkbox.click()

# Click the "Apply" button
apply = browser.find_element(By.XPATH, '//*[@id="contentarea_left"]/div[2]/form/div/div/div/a[1]')
apply.click()

# Crawl through pages
for idx in range(1, 40):
    browser.get(url + str(idx))

    # Extract data from the page
    df = pd.read_html(browser.page_source)[1]
    df.dropna(axis='index', how='all', inplace=True)  # Remove rows with all missing values
    df.dropna(axis='columns', how='all', inplace=True)  # Remove columns with all missing values

    # If no data is found, stop the crawl
    if len(df) == 0:
        break

    # Save the data to a CSV file
    f_name = 'fin.csv'
    if os.path.exists(f_name):
        df.to_csv(f_name, encoding='utf-8-sig', index=False, mode='a', header=False)
    else:
        df.to_csv(f_name, encoding='utf-8-sig', index=False)

    print(f'{idx} page completed')

# Close the browser
browser.quit()
```

---

## Future Improvements

1. **Handling Page Load Time**:
   - To ensure the page is fully loaded before extracting data, consider adding a wait time or use `WebDriverWait` with `expected_conditions` to wait for the page to load.

2. **Error Handling**:
   - Add exception handling to manage potential errors (e.g., network issues, missing elements) and prevent the script from crashing during execution.

## License

This script is open-source. Feel free to modify and use it for your own purposes. If you make improvements or fix bugs, contributions are always welcome!
