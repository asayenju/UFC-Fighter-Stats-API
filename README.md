# UFC Fighter Data API
This project consists of Python scripts for scraping data about UFC fighters from the official UFC website and an API build by flask.

## Overview
The project comprises the following components:

* scrape_urls.py: This script scrapes URLs of UFC fighters from the official UFC website using Selenium.
* scrape.py: This script scrapes detailed information about individual UFC fighters from their respective UFC profile pages using Requests and BeautifulSoup.
* app.py: This script serves as the main Python file for running the web application to display the scraped UFC fighter data.
* route.py: This script contains the routing logic for the Flask web application to serve scraped UFC fighter data.
* setup_db.py: Sets up the connection and creates the database in postgresql.
* insert.py: Calls scrape_urls.py and scrape.py to scrape the data and insert it into the database

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
cd UFC-Fighter-Stats-API
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

5. To build Docker image:
```bash
docker build -t ufc-fighter-stats-api .
```

6.Run the Docker container:
```bash
docker run -p 5000:5000 ufc-fighter-stats-api
```
You can access the API by a web browser.

# API Endpoints:
The following API Endpoints are available:

* Retrieve all fighters:
  - Endpoint: /api/fighters
  - HTTP Method: GET
  - Response: a JSON array of fighter objects

 * Retrieve a specific fighter by primary key id:
    - Endpoint: /api/fighters/id
    - HTTP Method: GET
    - Parameters: id of fighter
    - Response: JSON object containing the fighter’s details
  
  * Retrieve a specific fighter by name:
    - Endpoint: /api/fighters/name
    - HTTP Method: GET
    - Parameters: id of fighter
    - Response: JSON object containing the fighter’s details
   
  * Add a new fighter:
    - Endpoint: /api/fighters
    - HTTP Method: POST
    - Request: A JSON object containing fighter details
    - Response: A JSON object containing the created fighter details
    - Name, division, wins, draws and loss are required but everything else are option
    - You cannot add new keys to the dictionary to maintain data integrity

  * Update Fighter Details:
    - Endpoint: /api/fighters/<id>
    - HTTP Method: PUT
    - Description: Updates details of an existing fighter by ID.
    - Parameters: id: The ID of the fighter.
    - Request Body: A JSON object containing the updated details.
    - Response: A JSON object containing the updated fighter's details.
    - You can update details with existing keys


  * Delete a Fighter:
    - Endpoint: /api/fighters/<id>
    - HTTP Method: DELETE
    - Description: Deletes a fighter from the database by ID.
    - Parameters: id: The ID of the fighter.
    - Response: A confirmation message.
   
# All the keys in the object of a fighter:
* 'name': String of fighter's name
* 'id': Integer Primary key identifier
* 'division_title': String of weight class they are in
* 'win': Integer of wins
* 'loss': Integer of losses
* 'draw': Integer of draws
* 'trains_at': String of their training camp
* 'place_of_birth': String of their place of birth
* 'status': String of their status in the present 
* 'fight_style': String of fighting style
* 'age': Integer of age
* 'height': Float of height
* 'weight': Float of weight
* 'ufc_debut': String of the date of ufc debut
* 'reach': Float of their reach by hands
* 'leg_reach': Float of their leg reach
* 'wins_by_knockout': Integer of wins by knockout
* 'first_round_finishes': Integer of wins by first round finishes
* 'striking_accuracy_percent': Float of striking accuracy percentage
* 'significant_strikes_landed': Integer of significant strikes landed
* 'significant_strikes_attempted': Integer of significant strikes attempted
* 'takedown_accuracy_percent': Float of takedown accuracy percentage
* 'takedowns_landed': Integer of takedowns landed
* 'takedowns_attempted': Integer of takedowns attempted
* 'sig_str_landed_per_min': Float of significant strikes landed per minute
* 'sig_str_absorbed_per_min': Float of significant strikes absorber per min
* 'takedown_avg_per_15_min': Float of takedown average per 15 min
* 'submission_avg_per_15_min': Float of submission average per 15 min
* 'sig_str_defense_percent': Float of significant striking defense percentage
* 'takedown_defense_percent': Float of takedown defense percentage
* 'knockdown_avg': Float of knockdown average
* 'average_fight_time': String of average fight time
* 'sig_str_standing_amount': Integer of Signicant strikes when standing
* 'sig_str_clinch_amount': Integer of significant strikes when clinching
* 'sig_str_ground_amount': Integer of significant strikes when fighter is in ground
* 'win_by_ko_tko_amount': Win by knockout/technical knockout
* 'win_by_dec_amount': Win by decisions
* 'win_by_sub_amount': Win by submissions
* 'sig_str_standing_percentage': Float of significant strikes when standing percentage
* 'sig_str_clinch_percentage': Float of significant strikes when clinching percentage
* 'sig_str_ground_percentage': Float of significant strikes when fighter is in ground
* 'strike_to_head': Integer of strikes to head
* 'strike_to_head_per': Float of strikes to head percentage
* 'strike_to_body': Integer of strikes to body
* 'strike_to_body_per': Float of strikes to body percentage
* 'strike_to_leg': Integer of strikes to leg
* 'strike_to_leg_per': Float of strikes to leg precentage

  
# Directory Structure
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
  |   |-- setup_db.py
  |   |-- insert_data.py
  |-- /tests
  |   |-- test_scraping.py
  |   |-- test_api.py
  |-- requirements.txt
  |-- README.md

```





