# UFC Fighter Data API
This project consists of Python scripts for scraping data about UFC fighters from the official UFC website and a web application built using Flask to display the scraped data.

## Overview
The project comprises the following components:

* scrape_urls.py: This script scrapes URLs of UFC fighters from the official UFC website using Selenium.
* scrape.py: This script scrapes detailed information about individual UFC fighters from their respective UFC profile pages using Requests and BeautifulSoup.
* app.py: This script serves as the main Python file for running the web application to display the scraped UFC fighter data.
* route.py: This script contains the routing logic for the Flask web application to serve scraped UFC fighter data.
* Front-end Templates (HTML/CSS/JS): These templates are used for the front-end of the web application and display the scraped fighter data.

# Requirements

### To run the scripts and web application, you need to have the following dependencies installed:

* Python 3.12
* Flask
* Requests
* BeautifulSoup
* Selenium (for scrape_urls.py)
* Chrome WebDriver (for scrape_urls.py)
* psycopg2 (for fighters.py)
  
You can install the Python dependencies using pip:
```bash
pip install flask requests beautifulsoup4 selenium
```

## Installation and Usage
1. Cloning the Repository
```bash
git clone https://github.com/asayenju/UFC-Fighter-Stats-API.git
cd ufc-fighter-scraping
```
2. Download postgresql from https://www.postgresql.org/download/, make your port 5432 and password should be 1234.
3. Set up the database <br>
setup_db.py <br>
Run the code to set up and initialize the database

```bash
python setup_db.py
```

4. Scrape UFC Fighter Data and insert the data into the database <br>
insert.py <br>
Run the script using Python:
```bash
python insert.py
```
The script will scrape fighter urls and fighter data then insert into the database.

5. Running the Web Application
app.py<br>
Run the API using Python:
```bash
python app.py
```
You can access the API by a web browser.

Directory Structure
The directory structure of the project is as follows:

```arduino
/UFC-Fighter-Stats-API
  /ufc_fighter_stats
  |-- /scraping
  |   |-- scrape_ufc.py
  |   |-- scrape_urls.py
  |-- /api
  |   |-- app.py
  |   |-- /routes
  |       |-- fighters.py
  |-- /db
  |   |-- schema.sql
  |   |-- insert_data.py
  |-- /tests
  |   |-- test_scraping.py
  |   |-- test_api.py
  |-- requirements.txt
  |-- README.md

```


#API Endpoints:
The following API Endpoints are available:

* Retrieve all fighters:
  - Endpoint: /api/fighters
  - HTTP Method: GET
  - Response: a JSON array of fighter objects viewed in dictionaries


