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

#function that scrape data from an individual fighter's page
def scrape_fighter_data(fighter_url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(fighter_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Helper function to safely extract text from a tag
    def extract_text(tag):
        return tag.text.strip() if tag else 'N/A'
    
    # Extract fighter information
    name = extract_text(soup.find('h1', class_='hero-profile__name'))
    division_title = extract_text(soup.find('p', class_='hero-profile__division-title'))
    division_body = extract_text(soup.find('h1', class_='hero-profile__division-body'))
    win_loss_draw = division_body.split(' ')[0].split('-')
    win, loss, draw = map(int, win_loss_draw) if len(win_loss_draw) == 3 else (None, None, None)
    