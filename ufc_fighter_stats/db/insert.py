import psycopg2
import os
import sys
# Append the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scrapping.scrape import scrape_fighter_data
from scrapping.scrape_urls import get_fighter_urls

def insert_fighter():
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
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    fighter_urls = get_fighter_urls()
    for urls in fighter_urls:
        stats = scrape_fighter_data(urls)
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
    cursor.close()
    conn.close()

if __name__ == '__main__':
    insert_fighter()