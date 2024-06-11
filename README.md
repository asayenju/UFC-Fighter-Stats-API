# UFC Fighter Data API
This project consists of Python scripts for scraping data about UFC fighters from the official UFC website and a web application built using Flask to display the scraped data.

## Overview
The project comprises the following components:

scrape_urls.py: This script scrapes URLs of UFC fighters from the official UFC website using Selenium.
scrape.py: This script scrapes detailed information about individual UFC fighters from their respective UFC profile pages using Requests and BeautifulSoup.
app.py: This script serves as the main Python file for running the web application to display the scraped UFC fighter data.
route.py: This script contains the routing logic for the Flask web application to serve scraped UFC fighter data.
Front-end Templates (HTML/CSS/JS): These templates are used for the front-end of the web application and display the scraped fighter data.
Requirements

###To run the scripts and web application, you need to have the following dependencies installed:

Python 3.x
Flask
Requests
BeautifulSoup
Selenium (for scrape_urls.py)
Chrome WebDriver (for scrape_urls.py)
You can install the Python dependencies using pip:

```bash
pip install flask requests beautifulsoup4 selenium
```
Installation and Usage
1. Cloning the Repository
bash
Copy code
git clone <repository-url>
cd ufc-fighter-scraping
2. Scraping UFC Fighter URLs
scrape_urls.py
Ensure you have Chrome WebDriver installed and added to your system PATH.
Run the script using Python:
bash
Copy code
python scrape_urls.py
The script will automatically scrape the URLs of UFC fighters and save them to the specified directory.
3. Scraping UFC Fighter Data
scrape.py
Run the script using Python:
bash
Copy code
python scrape.py
The script will scrape fighter data from the specified URLs and output the information in a structured format.
4. Running the Web Application
app.py and route.py
Run the web application using Python:
bash
Copy code
python app.py
Access the web application through a browser.
Directory Structure
The directory structure of the project is as follows:

arduino
Copy code
ufc-fighter-scraping/
│
├── scrape_urls.py
├── scrape.py
├── app.py
├── route.py
├── templates/
│   ├── index.html
│   └── fighter.html
├── static/
│   └── style.css
└── README.md
Notes
Customize the front-end templates according to your design preferences.
Ensure proper error handling and data validation in route logic.
Modify the README files according to your specific project requirements and add more details as needed.
Feel free to reach out if you have any questions or need further assistance!
