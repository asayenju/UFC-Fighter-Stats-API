import requests

updated_data = {
    'name': 'Updated Fighter Name',
    'win': 20,
    'loss': 5,
    'draw': 1
    # Add other fields to update as needed
}

fighter_id = 2959  # The ID of the fighter you want to update
response = requests.put(f'http://127.0.0.1:5000/api/fighters/{fighter_id}', json=updated_data)

if response.status_code == 200:
    print("Fighter updated successfully")
else:
    print("Failed to update fighter:", response.json())