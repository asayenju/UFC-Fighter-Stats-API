import json

def test_get_all_fighters(client):
    response = client.get('/api/fighters')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)

def test_get_specific_fighter(client):
    response = client.get('/api/fighters/1')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, dict)
    assert data['id'] == 1

def test_add_new_fighter(client):
    new_fighter = {
        'name': 'Test Fighter',
        'division_title': 'Lightweight',
        'win': 10,
        'loss': 2,
        'draw': 1,
        'trains_at': 'Test Gym',
        'place_of_birth': 'Test City, Test Country',
        'status': 'Active',
        'fight_style': 'Striker',
        'age': 30,
        'height': 180,
        'weight': 70,
        'ufc_debut': '2020-01-01',
        'reach': 75,
        'leg_reach': 40,
        'wins_by_knockout': 7,
        'first_round_finishes': 5,
        'striking_accuracy_percent': 50.0,
        'significant_strikes_landed': 300,
        'significant_strikes_attempted': 600,
        'takedown_accuracy_percent': 40.0,
        'takedowns_landed': 20,
        'takedowns_attempted': 50,
        'sig_str_landed_per_min': 3.5,
        'sig_str_absorbed_per_min': 2.0,
        'takedown_avg_per_15_min': 2.0,
        'submission_avg_per_15_min': 1.0,
        'sig_str_defense_percent': 60.0,
        'takedown_defense_percent': 70.0,
        'knockdown_avg': 0.5,
        'average_fight_time': '10:00',
        'sig_str_standing_amount': 200,
        'sig_str_clinch_amount': 50,
        'sig_str_ground_amount': 50,
        'win_by_ko_tko_amount': 7,
        'win_by_dec_amount': 2,
        'win_by_sub_amount': 1,
        'sig_str_standing_percentage': 60.0,
        'sig_str_clinch_percentage': 20.0,
        'sig_str_ground_percentage': 20.0,
        'strike_to_head': 150,
        'strike_to_head_per': 50.0,
        'strike_to_body': 100,
        'strike_to_body_per': 33.3,
        'strike_to_leg': 50,
        'strike_to_leg_per': 16.7
    }
    response = client.post('/api/fighters', data=json.dumps(new_fighter), content_type='application/json')
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['name'] == 'Test Fighter'

def test_update_fighter(client):
    update_data = {
        'win': 11,
        'loss': 2,
        'draw': 1
    }
    response = client.put('/api/fighters/1', data=json.dumps(update_data), content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['win'] == 11

def test_delete_fighter(client):
    response = client.delete('/api/fighters/1')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['message'] == 'Fighter deleted successfully'