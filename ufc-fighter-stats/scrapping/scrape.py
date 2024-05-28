import requests
from bs4 import BeautifulSoup
import psycopg2
import psycopg2.extras
import json
import pandas as panda
import time

#function that returns fighter urls as a list
def get_fighter_urls(main_url, base_url):
    response = requests.get(main_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Example: Assume the fighter links are in <a> tags with href like '/athlete/athlete-name'
    links = soup.find_all('a', href=True)
    fighter_urls = [base_url + link['href'] for link in links if link['href'].startswith('/athlete/')]
    
    return fighter_urls

def scrape_fighter_data(fighter_url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(fighter_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Helper function to safely extract text from a tag
    def extract_text(tag):
        return tag.text.strip() if tag else 'N/A'
    
    def scrape_stats_records(soup):
        records = []
        stats_records = soup.find_all('div', class_='c-stat-compare__group')
        for stats_record in stats_records:
            compare_groups = stats_record.find_all('div', class_='c-stat-compare__group')
            record = {}
            for group in compare_groups:
                number_tag = group.find('div', class_='c-stat-compare__number')
                label_tag = group.find('div', class_='c-stat-compare__label')
                if number_tag and label_tag:
                    label = label_tag.text.strip()
                    number = number_tag.text.strip()
                    record[label] = number
            records.append(record)
        return records

    # Extract fighter information
    name = extract_text(soup.find('h1', class_='hero-profile__name'))
    division_title = extract_text(soup.find('p', class_='hero-profile__division-title'))
    division_body = extract_text(soup.find('h1', class_='hero-profile__division-body'))
    win_loss_draw = division_body.split(' ')[0].split('-')
    win, loss, draw = map(int, win_loss_draw) if len(win_loss_draw) == 3 else (None, None, None)

        # Extract striking accuracy data
    striking_accuracy_title_tag = soup.find('title', string='Striking accuracy')
    if striking_accuracy_title_tag:
        striking_accuracy_title = striking_accuracy_title_tag.string
        striking_accuracy_percent_tag = soup.find('text', class_='e-chart-circle__percent')
        if striking_accuracy_percent_tag:
            striking_accuracy_percent = int(striking_accuracy_percent_tag.string[:-1])

    # Extract significant strikes data
    sig_strikes_landed_tag = soup.find('dt', string='Sig. Strikes Landed')
    if sig_strikes_landed_tag:
        significant_strikes_landed = int(sig_strikes_landed_tag.find_next_sibling('dd').string)

    sig_strikes_attempted_tag = soup.find('dt', string='Sig. Strikes Attempted')
    if sig_strikes_attempted_tag:
        significant_strikes_attempted = int(sig_strikes_attempted_tag.find_next_sibling('dd').string)

    # Extract takedown accuracy data
    takedown_accuracy_title_tag = soup.find('title', string='Takedown Accuracy')
    if takedown_accuracy_title_tag:
        takedown_accuracy_title = takedown_accuracy_title_tag.string
        takedown_accuracy_percent_tag = soup.find('text', class_='e-chart-circle__percent')
        if takedown_accuracy_percent_tag:
            takedown_accuracy_percent = int(takedown_accuracy_percent_tag.string[:-1])

    takedowns_landed_tag = soup.find('dt', string='Takedowns Landed')
    if takedowns_landed_tag:
        takedowns_landed = int(takedowns_landed_tag.find_next_sibling('dd').string)

    takedowns_attempted_tag = soup.find('dt', string='Takedowns Attempted')
    if takedowns_attempted_tag:
        takedowns_attempted = int(takedowns_attempted_tag.find_next_sibling('dd').string)

    if striking_accuracy_percent == None:
        striking_accuracy_percent = (significant_strikes_landed/ significant_strikes_attempted) * 100

    if takedown_accuracy_percent == None:
        takedown_accuracy_percent = (takedowns_landed/ takedowns_attempted) * 100

    comparison_divs = soup.find_all('div', class_='c-stat-compare__group')
    significant_strikes_landed = float(comparison_divs[0].find('div', class_='c-stat-compare__number').text.strip())
    significant_strikes_absorbed_per_min = float(comparison_divs[1].find('div', class_='c-stat-compare__number').text.strip())
    takedown_avg_per_15_min = float(comparison_divs[2].find('div', class_='c-stat-compare__number').text.strip())
    submission_avg_per_15_min = float(comparison_divs[3].find('div', class_='c-stat-compare__number').text.strip())

    # Extract comparison stats
    comparison_div = soup.find_all('div', class_='c-stat-compare__group')
    significant_strikes_defense = float(comparison_div[0].find('div', class_='c-stat-compare__number').text.strip('%'))
    takedown_defense = float(comparison_div[1].find('div', class_='c-stat-compare__number').text.strip())  # Corrected
    knockdown_avg = float(comparison_div[2].find('div', class_='c-stat-compare__number').text.strip())
    average_fight_time = comparison_div[3].find('div', class_='c-stat-compare__number').text.strip()

    # Initialize specific stats
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
        'takedown_defense': None,
        'knockdown_avg': None,
        'average_fight_time': None
    }

    # Extract stats records
    records = scrape_stats_records(soup)
    for record in records:
        for key, value in record.items():
            if key in stats:
                stats[key] = int(value) if value.isdigit() else value

    return stats

# Test the function with a fighter URL
fighter_url = 'https://www.ufc.com/athlete/hamdy-abdelwahab'
print(scrape_fighter_data(fighter_url))

