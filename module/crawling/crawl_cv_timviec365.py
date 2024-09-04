# Import necessary libraries
import requests
import re
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import os
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from constant.config import DOMAIN_SELENIUM, DATABASE_NM, COLLECTION_NM_TV365, LIST_INFO_TV365
from database.connections_db import connect_db


# Function to crawl list of CV URLs from the TimViec365 website
def crawl_list_cv(web_url):
    # Set up Selenium driver with Chrome options
    capabilities = DesiredCapabilities.CHROME.copy()
    capabilities['goog:chromeOptions'] = {
        'args': [
            '--disable-extensions',    # Disable extensions
            '--no-sandbox',    # Bypass sandbox (may help avoid some issues)
            '--disable-dev-shm-usage',  # Reduce /dev/shm usage
            '--headless'  # Run in headless mode (if not needed)
        ]
    }
    driver = webdriver.Remote(
        command_executor=DOMAIN_SELENIUM,
        desired_capabilities=capabilities
    )

    try:
        # Navigate to the website
        driver.get(web_url)
        time.sleep(10)

        # Find and extract CV URLs
        elem = driver.find_elements(By.XPATH, "//a[@class='details_u_tit__rxCfN']")
        links = [el.get_attribute('href') for el in elem]

    finally:
        # Quit the driver
        driver.quit()

    return links


# Function to crawl CV image URLs from a given CV URL
def crawl_url_cv(link):
    response = requests.get(link)
    content = response.text

    pattern = r"https://storage\.timviec365\.vn/timviec365/pictures/cv/[^\s\"]+"
    matches = re.findall(pattern, content)

    return matches


# Function to download CV images from a list of URLs to a specified folder
def download_images(images_url, image_folder):
    os.makedirs(image_folder, exist_ok=True)

    for i, url in enumerate(images_url):
        response = requests.get(url)
        if response.status_code == 200:
            image_extension = url.split('.')[-1]
            image_path = os.path.join(image_folder, f"image{i + 1}.{image_extension}")
            with open(image_path, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded: {image_path}")
        else:
            print(f"Failed to download image from: {url}")


# Function to crawl and store CV information into a MongoDB database
def crawl_url_cv_info(link):
    # Connect to MongoDB
    client = connect_db()
    db = client[DATABASE_NM]
    collection = db[COLLECTION_NM_TV365]

    # Get the next sequence value for _id
    sequence = collection.find_one_and_update(
        {"_id": "cv_sequence"},
        {"$inc": {"value": 1}},
        upsert=True,
        return_document=True
    )
    _id = sequence["value"]

    # Convert string to list
    if LIST_INFO_TV365:
        variables = LIST_INFO_TV365.split(',')
    else:
        variables = []

    response = requests.get(link)
    content = response.text

    # main_pattern = r'"thong_tin":\s*(\{(?:[^{}]*|\{(?:[^{}]*|\{[^{}]*\})*\})*\})'
    # content_info = str(re.findall(main_pattern, content))

    # Define regular expression pattern to extract the required part from the content
    pattern = r''
    for variable in variables:
        pattern += fr'("{variable}":\s*(\d+|"[^"]+"))|'
    pattern = pattern.rstrip('|')

    matches = re.findall(pattern, content)
    cv_info = {"_id": _id}
    for match in matches:
        for value in match:
            if value:
                key = variables[match.index(value) // 2]
                cv_info[key] = value

    # Check if the document with the same _id already exists
    existing_cv = collection.find_one({"_id": _id})
    if existing_cv:
        # Update the existing document with the new data
        collection.update_one({"_id": _id}, {"$set": cv_info})
        print(f"Updated document with _id {_id}.")
    else:
        # Insert a new document
        collection.insert_one(cv_info)
        print(f"Inserted document with _id {_id}.")

    return cv_info