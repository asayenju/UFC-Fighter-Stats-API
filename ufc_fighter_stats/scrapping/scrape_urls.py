import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By


def get_fighter_urls():
    # Define the URL path and scraped files folder path
    global fighter_urls
    url_path = os.getcwd() + '/urls'
    file_path = os.getcwd() + '/scraped_files'

    # Create the file path if it doesn't exist
    os.makedirs(url_path, exist_ok=True)
    os.makedirs(file_path, exist_ok=True)

    # URL to scrape fighter data
    main_url = 'https://www.ufc.com/athletes/all'
    fighter_urls = []

    # Start a Selenium WebDriver session
    driver = webdriver.Chrome()  # You need to have Chrome WebDriver installed and added to PATH
    
    try:
        # Open the main URL
        driver.get(main_url)
        
        # Function to extract fighter URLs from the page source
        def extract_fighter_urls():
            links = driver.find_elements(By.CSS_SELECTOR, 'a[href^="/athlete/"]')
            for link in links:
                href = link.get_attribute('href')
                fighter_urls.append(href)

        # Extract initial fighter URLs
        extract_fighter_urls()

        # Click the "Load More" button until no more pages left
        while True:
            try:
                # Find the "Load More" button
                load_more_button = driver.find_element(By.XPATH, "//a[@title='Load more items']")
                
                # Extract the href attribute to construct the URL
                href = load_more_button.get_attribute('href')
                
                # Visit the next page
                driver.get(href)
                time.sleep(2)  # Add a short delay to avoid overwhelming the server
                
                # Extract fighter URLs from the new page
                extract_fighter_urls()
            except Exception as e:
                print(f"Error clicking 'Load More' button: {e}")
                break

    finally:
        # Close the WebDriver session
        driver.quit()

    return fighter_urls