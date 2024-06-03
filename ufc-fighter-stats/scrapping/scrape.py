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
        return tag.text.strip() if tag else 'N/A'

    def convert_to_float(percent_string):
        # Strip away the whitespace and the percentage sign
        clean_string = percent_string.strip().replace('%', '')
        # Convert the cleaned string to a float
        return float(clean_string)

    # Extract fighter information
    try:
        name = extract_text(soup.find('h1', class_='hero-profile__name'))
    except:
        name = None

    try:
        division_title = extract_text(soup.find('p', class_='hero-profile__division-title'))
    except:
        division_title = None

    try:
        division_body = extract_text(soup.find('h1', class_='hero-profile__division-body'))
    except:
        division_body = None

    try:
        # Find the <p> element by its class
        division_body = soup.find('p', class_='hero-profile__division-body')
        # Extract the text content
        division_text = division_body.text
        # Split the text to extract win, loss, and draw values
        win, loss, draw = map(int, division_text.split(' ')[0].split('-'))
    except:
        win = loss = draw = None

    # Initialize specific stats with None values
    wins_by_knockout = first_round_finishes = striking_accuracy_percent = None
    significant_strikes_landed = significant_strikes_attempted = takedown_accuracy_percent = None
    takedowns_landed = takedowns_attempted = significant_strikes_landed_per_min = None
    significant_strikes_absorbed_per_min = takedown_avg_per_15_min = submission_avg_per_15_min = None
    significant_strikes_defense = knockdown_avg = average_fight_time = trains_at = takedown_defense_perc = None

    try:
        # Extract stats
        stat_divs = soup.find_all('div', class_='hero-profile__stat')
        for stat_div in stat_divs:
            stat_value = int(extract_text(stat_div.find('p', class_='hero-profile__stat-numb')))
            stat_description = extract_text(stat_div.find('p', class_='hero-profile__stat-text'))

            # Assign to specific variables based on the description
            if stat_description == 'Wins by Knockout':
                wins_by_knockout = stat_value
            elif stat_description == 'First Round Finishes':
                first_round_finishes = stat_value
    except:
        pass

    try:
        # Extract striking accuracy data
        striking_accuracy_title_tag = soup.find('title', string='Striking accuracy')
        if striking_accuracy_title_tag:
            striking_accuracy_title = striking_accuracy_title_tag.string
            striking_accuracy_percent_tag = soup.find('text', class_='e-chart-circle__percent')
            if striking_accuracy_percent_tag:
                striking_accuracy_percent = int(striking_accuracy_percent_tag.string[:-1])
    except:
        pass

    try:
        # Extract significant strikes data
        sig_strikes_landed_tag = soup.find('dt', string='Sig. Strikes Landed')
        if sig_strikes_landed_tag:
            significant_strikes_landed = int(sig_strikes_landed_tag.find_next_sibling('dd').string)

        sig_strikes_attempted_tag = soup.find('dt', string='Sig. Strikes Attempted')
        if sig_strikes_attempted_tag:
            significant_strikes_attempted = int(sig_strikes_attempted_tag.find_next_sibling('dd').string)
    except:
        pass

    try:
        # Extract takedown accuracy data
        takedown_accuracy_title_tag = soup.find('title', string='Takedown Accuracy')
        if takedown_accuracy_title_tag:
            takedown_accuracy_title = takedown_accuracy_title_tag.string
            takedown_accuracy_percent_tag = soup.find('text', class_='e-chart-circle__percent')
            if takedown_accuracy_percent_tag:
                takedown_accuracy_percent = int(takedown_accuracy_percent_tag.string[:-1])

        takedowns_landed_tag = soup.find('dt', string='Takedowns Landed')
        try:
            if takedowns_landed_tag:
                takedowns_landed = int(takedowns_landed_tag.find_next_sibling('dd').string)
        except:
            takedowns_landed = None

        takedowns_attempted_tag = soup.find('dt', string='Takedowns Attempted')
        if takedowns_attempted_tag:
            takedowns_attempted = int(takedowns_attempted_tag.find_next_sibling('dd').string)

        if striking_accuracy_percent == None:
            striking_accuracy_percent = (significant_strikes_landed / significant_strikes_attempted) * 100

        if takedown_accuracy_percent == None and takedowns_landed != None and takedowns_attempted != None:
            takedown_accuracy_percent = (takedowns_landed / takedowns_attempted) * 100
    except:
        pass
    
    try:
        number_tags = soup.find_all('div', class_='c-stat-compare__number')

        values = []
        for tag in number_tags:
            value = tag.text.strip()
            values.append(value)

        significant_strikes_landed_per_min = float(values[0])
        significant_strikes_absorbed_per_min = float(values[1])
        takedown_avg_per_15_min = float(values[2])
        submission_avg_per_15_min = float(values[3])

        significant_strikes_defense = convert_to_float(values[4])
        takedown_defense_perc = convert_to_float(values[5])
        knockdown_avg = float(values[6])
        average_fight_time = values[7]
    except:
        pass
        print(number_tags)
    try:
        num_tags = soup.find_all('div', class_='c-stat-3bar__value')
        val = []
        for tag in num_tags:
            value = tag.text.strip()
            val.append(value)

        numbers = []
        percentages = []

        for item in val:
            # Split the item into the main number and the percentage part
            number, percentage = item.split(' ')
            # Remove the parentheses and the percentage sign
            percentage = percentage.strip('()%')
            # Convert both parts to integers and store them in respective lists
            numbers.append(int(number))
            percentages.append(int(percentage))

        significant_strikes_by_posstanding = numbers[0]
        significant_strikes_by_posclinching = numbers[1]
        significant_strikes_by_posground = numbers[2]
        w_by_ko_or_tko = numbers[3]
        w_by_decisions = numbers[4]
        w_by_submissions = numbers[5]

        significant_strikes_by_posstanding_per = percentages[0]
        significant_strikes_by_posclinching_per = percentages[1]
        significant_strikes_by_posground_per = percentages[2]
        w_by_ko_or_tko_per = percentages[3]
        w_by_decisions_per = percentages[4]
        w_by_submissions_per = percentages[5]
    except:
        significant_strikes_by_posstanding = significant_strikes_by_posclinching = significant_strikes_by_posground = None
        w_by_ko_or_tko = w_by_decisions = w_by_submissions = None
        significant_strikes_by_posstanding_per = significant_strikes_by_posclinching_per = significant_strikes_by_posground_per = None
        w_by_ko_or_tko_per = w_by_decisions_per = w_by_submissions_per = None

    try:
        strike_to_head = int(soup.find('text', id='e-stat-body_x5F__x5F_head_value').text)
        strike_to_head_per = float(soup.find('text', id='e-stat-body_x5F__x5F_head_percent').text.strip('%'))
        strike_to_body = int(soup.find('text', id='e-stat-body_x5F__x5F_body_value').text)
        strike_to_body_per = float(soup.find('text', id='e-stat-body_x5F__x5F_body_percent').text.strip('%'))
        strike_to_leg = int(soup.find('text', id='e-stat-body_x5F__x5F_leg_value').text)
        strike_to_leg_per = float(soup.find('text', id='e-stat-body_x5F__x5F_leg_percent').text.strip('%'))
    except:
        strike_to_head = strike_to_head_per = strike_to_body = strike_to_body_per = strike_to_leg = strike_to_leg_per = None

    try:
        nametags = soup.find_all('div', class_="c-bio__text")
        values = []
        for tag in nametags:
            value = tag.text.strip()
            values.append(value)

        if len(values) == 10:
            status = values[0]
            place_of_birth = values[1]
            trains_at = values[2]
            fight_style = values[3]
            age = float(values[4])
            height = float(values[5])
            weight = float(values[6])
            ufc_debut = values[7]
            reach = float(values[8])
            leg_reach = float(values[8])
        elif len(values) == 9:
            status = values[0]
            place_of_birth = values[1]
            fight_style = values[2]
            age = int(values[3])
            height = float(values[4])
            weight = float(values[5])
            ufc_debut = values[6]
            reach = float(values[7])
            leg_reach = float(values[8])
        else:
            status = place_of_birth = trains_at = fight_style = age = height = weight = ufc_debut = reach = leg_reach = None
    except:
        status = place_of_birth = trains_at = fight_style = age = height = weight = ufc_debut = reach = leg_reach = None

    return {
        'name': name,
        'division_title': division_title,
        'place_of_birth': place_of_birth,
        'status': status,
        'trains_at': trains_at,
        'fight_style': fight_style,
        'age': age,
        'height': height,
        'weight': weight,
        'ufc_debut': ufc_debut,
        'reach': reach,
        'leg_reach': leg_reach,
        'win': win,
        'loss': loss,
        'draw': draw,
        'wins_by_knockout': wins_by_knockout,
        'first_round_finishes': first_round_finishes,
        'striking_accuracy_percent': striking_accuracy_percent,
        'significant_strikes_landed': significant_strikes_landed,
        'significant_strikes_attempted': significant_strikes_attempted,
        'takedown_accuracy_percent': takedown_accuracy_percent,
        'takedowns_landed': takedowns_landed,
        'takedowns_attempted': takedowns_attempted,
        'significant_strikes_landed_per_min': significant_strikes_landed_per_min,
        'significant_strikes_absorbed_per_min': significant_strikes_absorbed_per_min,
        'takedown_avg_per_15_min': takedown_avg_per_15_min,
        'submission_avg_per_15_min': submission_avg_per_15_min,
        'significant_strikes_defense': significant_strikes_defense,
        'take_down_defense_perc': takedown_defense_perc,
        'knockdown_avg': knockdown_avg,
        'average_fight_time': average_fight_time,
        'significant_strikes_by_standing_position': significant_strikes_by_posstanding,
        'significant_strikes_by_standing_position_per': significant_strikes_by_posstanding_per,
        'significant_strikes_by_clinching_position': significant_strikes_by_posclinching,
        'significant_strikes_by_clinching_position_per': significant_strikes_by_posclinching_per,
        'significant_strikes_by_ground_position': significant_strikes_by_posground,
        'significant_strikes_by_ground_position_per': significant_strikes_by_posground_per,
        'w_by_ko_or_tko': w_by_ko_or_tko,
        'w_by_ko_or_tko_per': w_by_ko_or_tko_per,
        'w_by_decisions': w_by_decisions,
        'w_by_decisions_per': w_by_decisions_per,
        'w_by_submissions': w_by_submissions,
        'w_by_submissions_per': w_by_submissions_per,
        'strike_to_head': strike_to_head,
        'strike_to_head_per': strike_to_head_per,
        'strike_to_body': strike_to_body,
        'strike_to_body_per': strike_to_body_per,
        'strike_to_leg': strike_to_leg,
        'strike_to_leg_per': strike_to_leg_per,
    }

# Test the function with a fighter URL

fighter_url = 'https://www.ufc.com/athlete/john-adajar'
print(scrape_fighter_data(fighter_url))

#Test function that stores all fighter url in an array
main_url = 'https://www.ufc.com/athletes/all'
base_url = 'https://www.ufc.com/athletes'
#get_fighter_urls()
#print(f"Total fighter URLs found: {len(fighter_urls)}")
#for i in range(len(fighter_urls)):
    #scrape_fighter_data(fighter_urls[i])