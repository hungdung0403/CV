import time
import re
import json
import datetime
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from constant.config import DOMAIN_SELENIUM, COLLECTION_NM_ITVIEC, DATABASE_NM
from database.connections_db import connect_db


def crawl_list_job(web_url):
    """
    This function crawls the list of job URLs from the ITViec website.

    Args:
    driver_path (str): The path to the ChromeDriver executable.
    web_url (str): The URL of the ITViec website.

    Returns:
    list: A list of job URLs.
    """
    # driver = webdriver.Chrome(driver_path)
    # Set up connection with Selenium Server
    capabilities = DesiredCapabilities.CHROME.copy()

    # Add some options to improve stability
    capabilities['goog:chromeOptions'] = {
        'args': [
            '--disable-extensions',  # Disable extensions
            '--no-sandbox',  # Bypass sandbox (may help avoid some issues)
            '--disable-dev-shm-usage',  # Reduce /dev/shm usage
            # '--headless'  # Run in headless mode (if not needed)
        ]
    }
    driver = webdriver.Remote(
        command_executor=DOMAIN_SELENIUM,
        desired_capabilities=capabilities
    )
    try:
        # Clear cookies
        driver.delete_all_cookies()

        driver.get(web_url)

        # List of job URLs
        links = set()

        # Crawl job URLs until the desired number of pages is reached
        while True:
            # Find job URLs on the current page
            elem = driver.find_elements(By.XPATH, "//a[@class='text-it-black']")
            print(f"Current page URL: {driver.current_url}")
            print(f"Number of next_page_button elements found: {len(elem)}")
            page_links = [el.get_attribute('href') for el in elem]
            links.update(page_links)
            print(f"Current number of pages saved: {len(links)}")

            # Check for the "page next" class
            next_page_button = driver.find_elements(By.CSS_SELECTOR, 'div.page.next a[rel="next"]')

            # Get page number from the URL, needed when limiting the number of pages
            # pattern = r'page=(\d+)'
            # page_number = re.search(pattern, next_page_button[0].get_attribute('href'))

            if next_page_button: # and int(page_number.group(1)) <= 3:
                # Get the href attribute of the "page next" button
                next_page_link = next_page_button[0].get_attribute('href')
                print(f"Next page URL: {next_page_link}")

                # Quit the current driver instance and create a new one
                driver.quit()
                driver = webdriver.Remote(
                    command_executor=DOMAIN_SELENIUM,
                    desired_capabilities=capabilities
                )
                # Clear cookies
                driver.delete_all_cookies()

                # Navigate to the next page
                driver.get(next_page_link)

            else:
                # No more pages to navigate, break the loop
                break
        print(list(links))
        return list(links)
    finally:
        driver.quit()


def crawl_url_job(link):
    """
    This function crawls the job details page and stores the data in MongoDB.

    Args:
    link (str): The URL of the job details page.
    """
    # Set up connection with Selenium Server
    capabilities = DesiredCapabilities.CHROME.copy()

    # Add some options to improve stability
    capabilities['goog:chromeOptions'] = {
        'args': [
            '--disable-extensions',  # Disable extensions
            '--no-sandbox',  # Bypass sandbox (may help avoid some issues)
            '--disable-dev-shm-usage',  # Reduce /dev/shm usage
            # '--headless'  # Run in headless mode (if not needed)
        ]
    }
    driver = webdriver.Remote(
        command_executor=DOMAIN_SELENIUM,
        desired_capabilities=capabilities
    )

    # Connect to MongoDB
    client = connect_db()
    db = client[DATABASE_NM]
    collection = db[COLLECTION_NM_ITVIEC]

    # Get the next sequence value for _id
    sequence = collection.find_one_and_update(
        {"_id": "job_sequence"},
        {"$inc": {"value": 1}},
        upsert=True,
        return_document=True
    )
    _id = sequence["value"]

    try:
        # Clear cookies
        driver.delete_all_cookies()

        driver.get(link)
        content = driver.page_source
        main_pattern = r'''<main\s+class=['"]d-flex\s+flex-column\s+min-vh-main['"]>\s*<div\s+class=['"]flex-grow-1['"]>\s*<script\s+type=['"]application/ld\+json['"]>\s*({.*?})\s*</script>'''
        content_info = str(re.findall(main_pattern, content))

        # Replace unnecessary characters and convert JSON string to JSON object
        json_str = content_info.replace("['", '[').replace("']", ']')
        json_str = json_str.replace('\\\\', '\\')
        json_str = json_str.replace("\\'", "'")
        json_object = []
        # Try to convert to JSON object
        try:
            json_object = json.loads(json_str)
        except json.decoder.JSONDecodeError as e:
            # Print error message with error position
            print(f"Error JSONDecodeError: {e}")
        else:
            print(json.dumps(json_object, indent=4))

        # Get data datePosted
        pattern = r'"datePosted":"(\d{4}-\d{2}-\d{2})"'
        date_posted = re.findall(pattern, json_str)
        first_date_posted = date_posted[0] if date_posted else None

        # Get current date
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")

        # Check if data is empty and the date posted is today
        if json_object and first_date_posted == current_date:
            # Insert data into MongoDB if data is not empty
            collection.insert_many(json_object)
            print("Data has been inserted into MongoDB.")
        else:
            print("Empty data, no insert into MongoDB.")
    finally:
        driver.quit()
