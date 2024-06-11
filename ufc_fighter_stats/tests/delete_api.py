import requests

# Define the URL of the API endpoint
url = 'http://127.0.0.1:5000/api/fighters'
fighter_id = 2960
response = requests.delete(f'http://127.0.0.1:5000/api/fighters/{fighter_id}', json=fighter_id)

if response.status_code == 200:
    print("Fighter deleted successfully")
else:
    print("Failed to delete fighter:", response.json())
