import psycopg2
import os
import sys

# Append the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scrapping.scrape import scrape_fighter_data
from scrapping.scrape_urls import get_fighter_urls

def insert_fighter(stats):
    conn = psycopg2.connect(
        dbname="ufc_fighter_data",
        user="postgres",
        password="1234",
        host="localhost"
    )
    cursor = conn.cursor()
    
    insert_query = '''
    INSERT INTO fighters (
        name, division_title, win, loss, draw, trains_at, place_of_birth,
        status, fight_style, age, height, weight, ufc_debut, reach, leg_reach,
        wins_by_knockout, first_round_finishes, striking_accuracy_percent,
        significant_strikes_landed, significant_strikes_attempted,
        takedown_accuracy_percent, takedowns_landed, takedowns_attempted,
        sig_str_landed_per_min, sig_str_absorbed_per_min, takedown_avg_per_15_min,
        submission_avg_per_15_min, sig_str_defense_percent, takedown_defense_percent,
        knockdown_avg, average_fight_time, sig_str_standing_amount, sig_str_clinch_amount,
        sig_str_ground_amount, win_by_ko_tko_amount, win_by_dec_amount, win_by_sub_amount,
        sig_str_standing_percentage, sig_str_clinch_percentage, sig_str_ground_percentage,
        strike_to_head, strike_to_head_per, strike_to_body, strike_to_body_per, strike_to_leg, strike_to_leg_per
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    
    # Ensure all keys are present in the stats dictionary, and provide defaults for missing keys
    required_keys = [
        'name', 'division_title', 'win', 'loss', 'draw', 'trains_at', 'place_of_birth',
        'status', 'fight_style', 'age', 'height', 'weight', 'ufc_debut', 'reach', 'leg_reach',
        'wins_by_knockout', 'first_round_finishes', 'striking_accuracy_percent',
        'significant_strikes_landed', 'significant_strikes_attempted',
        'takedown_accuracy_percent', 'takedowns_landed', 'takedowns_attempted',
        'sig_str_landed_per_min', 'sig_str_absorbed_per_min', 'takedown_avg_per_15_min',
        'submission_avg_per_15_min', 'sig_str_defense_percent', 'takedown_defense_percent',
        'knockdown_avg', 'average_fight_time', 'sig_str_standing_amount', 'sig_str_clinch_amount',
        'sig_str_ground_amount', 'win_by_ko_tko_amount', 'win_by_dec_amount', 'win_by_sub_amount',
        'sig_str_standing_percentage', 'sig_str_clinch_percentage', 'sig_str_ground_percentage',
        'strike_to_head', 'strike_to_head_per', 'strike_to_body', 'strike_to_body_per', 'strike_to_leg', 'strike_to_leg_per'
    ]
    
    for key in required_keys:
        if key not in stats:
            stats[key] = None
    
    try:
        cursor.execute(insert_query, (
            stats['name'], stats['division_title'], stats['win'], stats['loss'], stats['draw'], 
            stats['trains_at'], stats['place_of_birth'], stats['status'], stats['fight_style'], 
            stats['age'], stats['height'], stats['weight'], stats['ufc_debut'], stats['reach'], 
            stats['leg_reach'], stats['wins_by_knockout'], stats['first_round_finishes'], 
            stats['striking_accuracy_percent'], stats['significant_strikes_landed'], 
            stats['significant_strikes_attempted'], stats['takedown_accuracy_percent'], 
            stats['takedowns_landed'], stats['takedowns_attempted'], stats['sig_str_landed_per_min'], 
            stats['sig_str_absorbed_per_min'], stats['takedown_avg_per_15_min'], 
            stats['submission_avg_per_15_min'], stats['sig_str_defense_percent'], 
            stats['takedown_defense_percent'], stats['knockdown_avg'], stats['average_fight_time'], 
            stats['sig_str_standing_amount'], stats['sig_str_clinch_amount'], 
            stats['sig_str_ground_amount'], stats['win_by_ko_tko_amount'], stats['win_by_dec_amount'], 
            stats['win_by_sub_amount'], stats['sig_str_standing_percentage'], 
            stats['sig_str_clinch_percentage'], stats['sig_str_ground_percentage'], 
            stats['strike_to_head'], stats['strike_to_head_per'], stats['strike_to_body'], 
            stats['strike_to_body_per'], stats['strike_to_leg'], stats['strike_to_leg_per']
        ))
        
        conn.commit()
    except psycopg2.Error as e:
        print(f"Error inserting data: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    stats = {
        'name': 'Fighter Name',
        'division_title': 'Lightweight',
        'win': 10,
        'loss': 2,
        'draw': 1,
        'trains_at': 'Gym Name',
        'place_of_birth': 'City, Country',
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
    print(len(stats))
    insert_fighter(stats)