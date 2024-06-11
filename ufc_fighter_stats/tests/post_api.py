import requests

# Define the URL of the API endpoint
url = 'http://127.0.0.1:5000/api/fighters'

# Define the fighter's details as a dictionary
fighter_data = {
    'name': 'Ashwin Sayenju',
    'division_title': 'Middleweight',
    'win': 15,
    'loss': 5,
    'draw': 1
    # Add other attributes as needed
}

# Send a POST request to create the fighter
response = requests.post(url, json=fighter_data)

# Check the response status
if response.status_code == 201:
    print("Fighter created successfully!")
    print("Fighter ID:", response.json()['fighter_id'])
else:
    print("Failed to create fighter:", response.json())