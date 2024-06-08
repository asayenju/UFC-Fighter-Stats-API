import requests
from bs4 import BeautifulSoup
import psycopg2
import psycopg2.extras
import json
import pandas as panda
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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


def scrape_fighter_data(fighter_url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(fighter_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Helper function to safely extract text from a tag
    def extract_text(tag):
        return tag.text.strip() if tag else None

    def convert_to_float(percent_string):
        try:
            clean_string = percent_string.strip().replace('%', '')
            return float(clean_string)
        except (ValueError, AttributeError):
            return None

    # Extract fighter information
    name = extract_text(soup.find('h1', class_='hero-profile__name'))
    division_title = extract_text(soup.find('p', class_='hero-profile__division-title'))
    division_body = extract_text(soup.find('h1', class_='hero-profile__division-body'))

    try:
        division_body = soup.find('p', class_='hero-profile__division-body')
        division_text = division_body.text
        win, loss, draw = map(int, division_text.split(' ')[0].split('-'))
    except:
        win, loss, draw = None, None, None

    stats = {
        'name': name,
        'division_title': division_title,
        'win': win,
        'loss': loss,
        'draw': draw,
        'wins_by_knockout': None,
        'first_round_finishes': None,
        'striking_accuracy_percent': None,
        'significant_strikes_landed': None,
        'significant_strikes_attempted': None,
        'takedown_accuracy_percent': None,
        'takedowns_landed': None,
        'takedowns_attempted': None,
        'significant_strikes_landed_per_min': None,
        'significant_strikes_absorbed_per_min': None,
        'takedown_avg_per_15_min': None,
        'submission_avg_per_15_min': None,
        'significant_strikes_defense': None,
        'knockdown_avg': None,
        'average_fight_time': None,
        'trains_at': None,
        'place_of_birth': None,
        'status': None,
        'fight_style': None,
        'age': None,
        'height': None,
        'weight': None,
        'ufc_debut': None,
        'reach': None,
        'leg_reach': None,
        'significant_strikes_by_posstanding': None,
        'significant_strikes_by_posclinching': None,
        'significant_strikes_by_posground': None,
        'w_by_ko_or_tko': None,
        'w_by_decisions': None,
        'w_by_submissions': None,
        'significant_strikes_by_posstanding_per': None,
        'significant_strikes_by_posclinching_per': None,
        'significant_strikes_by_posground_per': None,
        'w_by_ko_or_tko_per': None,
        'w_by_decisions_per': None,
        'w_by_submissions_per': None,
        'strike_to_head': None,
        'strike_to_head_per': None,
        'strike_to_body': None,
        'strike_to_body_per': None,
        'strike_to_leg': None,
        'strike_to_leg_per': None
    }

    try:
        stat_divs = soup.find_all('div', class_='hero-profile__stat')
        for stat_div in stat_divs:
            stat_value = int(extract_text(stat_div.find('p', class_='hero-profile__stat-numb')))
            stat_description = extract_text(stat_div.find('p', class_='hero-profile__stat-text'))

            if stat_description == 'Wins by Knockout':
                stats['wins_by_knockout'] = stat_value
            elif stat_description == 'First Round Finishes':
                stats['first_round_finishes'] = stat_value
    except:
        pass

    try:
        # Find all <text> elements with class 'e-chart-circle__percent'
        percent_elements = soup.find_all('text', class_='e-chart-circle__percent')

        # Initialize variables to store accuracy percentages
        striking_accuracy_percentage = None
        takedown_accuracy_percentage = None

        # Iterate through the <text> elements
        for element in percent_elements:
            # Extract the accuracy percentage value
            accuracy_percentage = element.get_text().strip()

            # Check if it represents striking accuracy or takedown accuracy
            if 'Striking accuracy' in element.parent.find('title').get_text():
                striking_accuracy_percentage = convert_to_float(accuracy_percentage)
            elif 'Takedown Accuracy' in element.parent.find('title').get_text():
                takedown_accuracy_percentage = convert_to_float(accuracy_percentage)

        # Store accuracy percentages in the stats dictionary
        stats['striking_accuracy_percent'] = striking_accuracy_percentage
        stats['takedown_accuracy_percent'] = takedown_accuracy_percentage

    except Exception as e:
        print("An error occurred while parsing accuracy percentages:", e)

    try:
        # Find the div for striking accuracy
        striking_accuracy_h2_tag = soup.find('h2', class_='e-t3', string='Striking accuracy')

        # Navigate to its parent div tag
        if striking_accuracy_h2_tag:
            striking_accuracy_title_tag = striking_accuracy_h2_tag.parent
        else:
            raise ValueError("Striking Accuracy title tag not found.")

        # Find significant strikes landed and attempted
        striking_dl = striking_accuracy_title_tag.find_next_sibling('div', class_='c-overlap__stats-wrap')
        if striking_dl:
            sig_strikes_landed_tag = striking_dl.find('dt', class_='c-overlap__stats-text', string='Sig. Strikes Landed')
            if sig_strikes_landed_tag:
                sig_strikes_landed = sig_strikes_landed_tag.find_next_sibling('dd', class_='c-overlap__stats-value').text.strip()
                # Check if sig_strikes_landed is blank, if so, set it to None
                sig_strikes_landed = None if not sig_strikes_landed else int(sig_strikes_landed)
                stats['significant_strikes_landed'] = sig_strikes_landed

            # Find significant strikes attempted
            sig_strikes_attempted_tag = striking_dl.find('dt', class_='c-overlap__stats-text', string='Sig. Strikes Attempted')
            if sig_strikes_attempted_tag:
                sig_strikes_attempted = sig_strikes_attempted_tag.find_next_sibling('dd', class_='c-overlap__stats-value').text.strip()
                # Check if sig_strikes_attempted is blank, if so, set it to None
                sig_strikes_attempted = None if not sig_strikes_attempted else int(sig_strikes_attempted)
                stats['significant_strikes_attempted'] = sig_strikes_attempted

    except Exception as e:
        print("An error occurred while parsing striking accuracy stats:", e)

    try:
        # Find the div for takedown accuracy
        takedown_accuracy_h2_tag = soup.find('h2', class_='e-t3', string='Takedown Accuracy')

        # Navigate to its parent div tag
        if takedown_accuracy_h2_tag:
            takedown_accuracy_title_tag = takedown_accuracy_h2_tag.parent
        else:
            raise ValueError("Takedown Accuracy title tag not found.")

        # Find takedowns landed and attempted
        takedown_dl = takedown_accuracy_title_tag.find_next_sibling('div', class_='c-overlap__stats-wrap')
        if takedown_dl:
            takedowns_landed_tag = takedown_dl.find('dt', class_='c-overlap__stats-text', string='Takedowns Landed')
            if takedowns_landed_tag:
                takedowns_landed = takedowns_landed_tag.find_next_sibling('dd', class_='c-overlap__stats-value').text.strip()
                # Check if takedowns_landed is blank, if so, set it to None
                takedowns_landed = None if not takedowns_landed else int(takedowns_landed)
                stats['takedowns_landed'] = takedowns_landed

            # Find takedowns attempted
            takedowns_attempted_tag = takedown_dl.find('dt', class_='c-overlap__stats-text', string='Takedowns Attempted')
            if takedowns_attempted_tag:
                takedowns_attempted = takedowns_attempted_tag.find_next_sibling('dd', class_='c-overlap__stats-value').text.strip()
                # Check if takedowns_attempted is blank, if so, set it to None
                takedowns_attempted = None if not takedowns_attempted else int(takedowns_attempted)
                stats['takedowns_attempted'] = takedowns_attempted

    except Exception as e:
        print("An error occurred while parsing takedown accuracy stats:", e)

    if stats['striking_accuracy_percent'] is None and stats['significant_strikes_landed'] is not None and stats['significant_strikes_attempted'] is not None:
        stats['striking_accuracy_percent'] = (stats['significant_strikes_landed'] / stats['significant_strikes_attempted']) * 100

    if stats['takedown_accuracy_percent'] is None and stats['takedowns_landed'] is not None and stats['takedowns_attempted'] is not None:
        stats['takedown_accuracy_percent'] = (stats['takedowns_landed'] / stats['takedowns_attempted']) * 100


    try:
        number_tags = soup.find_all('div', class_='c-stat-compare__number')
        values = [tag.text.strip() for tag in number_tags]

        stats['significant_strikes_landed_per_min'] = float(values[0])
        stats['significant_strikes_absorbed_per_min'] = float(values[1])
        stats['takedown_avg_per_15_min'] = float(values[2])
        stats['submission_avg_per_15_min'] = float(values[3])
        stats['significant_strikes_defense'] = convert_to_float(values[4])
        stats['knockdown_avg'] = convert_to_float(values[5])
        stats['average_fight_time'] = values[6]
    except:
        pass

    try:
        num_tags = soup.find_all('div', class_='c-stat-3bar__value')
        val = [tag.text.strip() for tag in num_tags]

        numbers = []
        percentages = []

        for item in val:
            parts = item.split(' ')
            number = parts[0]
            percentage = parts[1] if len(parts) > 1 else '0%'
            percentage = percentage.strip('()%')
            numbers.append(int(number))
            percentages.append(int(percentage))

        stats['significant_strikes_by_posstanding'] = numbers[0]
        stats['significant_strikes_by_posclinching'] = numbers[1]
        stats['significant_strikes_by_posground'] = numbers[2]
        stats['w_by_ko_or_tko'] = numbers[3]
        stats['w_by_decisions'] = numbers[4]
        stats['w_by_submissions'] = numbers[5]
        stats['significant_strikes_by_posstanding_per'] = percentages[0]
        stats['significant_strikes_by_posclinching_per'] = percentages[1]
        stats['significant_strikes_by_posground_per'] = percentages[2]
        stats['w_by_ko_or_tko_per'] = percentages[3]
        stats['w_by_decisions_per'] = percentages[4]
        stats['w_by_submissions_per'] = percentages[5]
    except:
        pass

    try:
        stats['strike_to_head'] = int(soup.find('text', id='e-stat-body_x5F__x5F_head_value').text)
        stats['strike_to_head_per'] = float(soup.find('text', id='e-stat-body_x5F__x5F_head_percent').text.strip('%'))
        stats['strike_to_body'] = int(soup.find('text', id='e-stat-body_x5F__x5F_body_value').text)
        stats['strike_to_body_per'] = float(soup.find('text', id='e-stat-body_x5F__x5F_body_percent').text.strip('%'))
        stats['strike_to_leg'] = int(soup.find('text', id='e-stat-body_x5F__x5F_leg_value').text)
        stats['strike_to_leg_per'] = float(soup.find('text', id='e-stat-body_x5F__x5F_leg_percent').text.strip('%'))
    except:
        pass

    return stats

# Test the function with a fighter URL

fighter_url = 'https://www.ufc.com/athlete/israel-adesanya'
print(scrape_fighter_data(fighter_url))

#Test function that stores all fighter url in an array
main_url = 'https://www.ufc.com/athletes/all'
base_url = 'https://www.ufc.com/athletes'
#get_fighter_urls()
#print(f"Total fighter URLs found: {len(fighter_urls)}")
#for i in range(len(fighter_urls)):
    #scrape_fighter_data(fighter_urls[i])