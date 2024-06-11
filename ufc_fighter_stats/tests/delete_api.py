import requests

# Define the URL of the API endpoint
url = 'http://127.0.0.1:5000/api/fighters'
fighter_id = 2959
response = requests.post(url, json=fighter_id)

