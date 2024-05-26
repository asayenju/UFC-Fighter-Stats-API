import requests
from bs4 import BeautifulSoup
import psycopg2
import psycopg2.extras
import json
import pandas as panda
import time

def get_fighter_urls(main_url, base_url):
    response = requests.get(main_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Example: Assume the fighter links are in <a> tags with href like '/athlete/athlete-name'
    links = soup.find_all('a', href=True)
    fighter_urls = [base_url + link['href'] for link in links if link['href'].startswith('/athlete/')]
    
    return fighter_urls
