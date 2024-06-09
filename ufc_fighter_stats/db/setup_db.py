import psycopg2


def create_database():
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="1234",
        host="localhost"
    )
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE ufc_fighter_data")
    cursor.close()
    conn.close()

def create_tables():
    conn = psycopg2.connect(
        dbname="ufc_fighter_data",
        user="postgres",
        password="1234",
        host="localhost"
    )
    cursor = conn.cursor()
    schema_sql = """
    CREATE TABLE fighters (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        division_title TEXT,
        win INTEGER,
        loss INTEGER,
        draw INTEGER,
        trains_at TEXT,
        place_of_birth TEXT,
        status TEXT,
        fight_style TEXT,
        age INTEGER,
        height REAL,
        weight REAL,
        ufc_debut TEXT,
        reach REAL,
        leg_reach REAL,
        wins_by_knockout INTEGER,
        first_round_finishes INTEGER,
        striking_accuracy_percent REAL,
        significant_strikes_landed INTEGER,
        significant_strikes_attempted INTEGER,
        takedown_accuracy_percent REAL,
        takedowns_landed INTEGER,
        takedowns_attempted INTEGER,
        sig_str_landed_per_min REAL,
        sig_str_absorbed_per_min REAL,
        takedown_avg_per_15_min REAL,
        submission_avg_per_15_min REAL,
        sig_str_defense_percent REAL,
        takedown_defense_percent REAL,
        knockdown_avg REAL,
        average_fight_time TEXT,
        sig_str_standing_amount INTEGER,
        sig_str_clinch_amount INTEGER,
        sig_str_ground_amount INTEGER,
        win_by_ko_tko_amount INTEGER,
        win_by_dec_amount INTEGER,
        win_by_sub_amount INTEGER,
        sig_str_standing_percentage REAL,
        sig_str_clinch_percentage REAL,
        sig_str_ground_percentage REAL,
        strike_to_head INTEGER,
        strike_to_head_per REAL,
        strike_to_body INTEGER,
        strike_to_body_per REAL,
        strike_to_leg INTEGER,
        strike_to_leg_per REAL
    );
    """
    cursor.execute(schema_sql)
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    create_database()
    create_tables()
