from flask import Flask, jsonify, request
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
db_config = {
    'dbname': 'ufc_fighter_data',
    'user': 'postgres',
    'password': '1234',
    'host': 'db'
}

# Function to establish database connection
def connect_db():
    try:
        conn = psycopg2.connect(**db_config)
        return conn
    except psycopg2.Error as e:
        # Handle connection errors
        print("Database connection error:", e)
        return None
    

@app.route('/')
def home():
    return "Welcome to UFC fighter Stats API"

def reorder_fighter_data(fighter):
    reordered_fighter = {'id': fighter['id'], 'name': fighter['name']}
    reordered_fighter.update({k: v for k, v in fighter.items() if k not in ['id', 'name']})
    return reordered_fighter


@app.route('/api/fighters', methods=['GET'])
def get_fighters():
    try:
        conn = connect_db()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM fighters ORDER BY id")
            fighters = cur.fetchall()
            reordered_fighters = [reorder_fighter_data(fighter) for fighter in fighters]
        conn.close()
        return jsonify(reordered_fighters)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/fighters/<int:fighter_id>', methods=['GET'])
def get_fighter(fighter_id):
    try:
        conn = connect_db()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM fighters WHERE id = %s", (fighter_id,))
            fighter = cur.fetchone()
            if fighter is None:
                return jsonify({'error': 'Fighter not found'}), 404
        conn.close()
        reordered_fighter = reorder_fighter_data(fighter)
        return jsonify(reordered_fighter)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/fighters/<string:name>', methods=['GET'])
def get_fighter_by_name(name):
    try:
        conn = connect_db()
        if not conn:
            return jsonify({'error': 'Failed to connect to the database'}), 500

        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM fighters WHERE name = %s", (name,))
            fighter = cur.fetchone()
            if fighter is None:
                return jsonify({'error': 'Fighter not found'}), 404

        conn.close()
        reordered_fighter = reorder_fighter_data(fighter)
        return jsonify(reordered_fighter)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/fighters', methods=['POST'])
def create_fighter():
    try:
        stats = request.json

        # Validate input fields
        required_fields = ['name', 'division_title', 'win', 'loss', 'draw']
        for field in required_fields:
            if field not in stats:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        allowed_attributes = ['name', 'division_title', 'win', 'loss', 'draw', 'trains_at', 'place_of_birth',
                              'status', 'fight_style', 'age', 'height', 'weight', 'ufc_debut', 'reach', 'leg_reach',
                              'wins_by_knockout', 'first_round_finishes', 'striking_accuracy_percent',
                              'significant_strikes_landed', 'significant_strikes_attempted',
                              'takedown_accuracy_percent', 'takedowns_landed', 'takedowns_attempted',
                              'sig_str_landed_per_min', 'sig_str_absorbed_per_min', 'takedown_avg_per_15_min',
                              'submission_avg_per_15_min', 'sig_str_defense_percent', 'takedown_defense_percent',
                              'knockdown_avg', 'average_fight_time', 'sig_str_standing_amount', 'sig_str_clinch_amount',
                              'sig_str_ground_amount', 'win_by_ko_tko_amount', 'win_by_dec_amount', 'win_by_sub_amount',
                              'sig_str_standing_percentage', 'sig_str_clinch_percentage', 'sig_str_ground_percentage',
                              'strike_to_head', 'strike_to_head_per', 'strike_to_body', 'strike_to_body_per', 'strike_to_leg', 'strike_to_leg_per']

        optional_fields = {
            'age': None,
            'average_fight_time': None,
            'first_round_finishes': None,
            'height': None,
            'knockdown_avg': None,
            'leg_reach': None,
            'reach': None,
            'sig_str_absorbed_per_min': None,
            'sig_str_clinch_amount': None,
            'sig_str_clinch_percentage': None,
            'sig_str_ground_amount': None,
            'sig_str_ground_percentage': None,
            'sig_str_landed_per_min': None,
            'sig_str_standing_amount': None,
            'sig_str_standing_percentage': None,
            'sig_str_defense_percent': None,
            'significant_strikes_attempted': None,
            'significant_strikes_landed': None,
            'strike_to_body': None,
            'strike_to_body_per': None,
            'strike_to_head': None,
            'strike_to_head_per': None,
            'strike_to_leg': None,
            'strike_to_leg_per': None,
            'striking_accuracy_percent': None,
            'submission_avg_per_15_min': None,
            'takedown_accuracy_percent': None,
            'takedown_avg_per_15_min': None,
            'takedown_defense_percent': None,
            'takedowns_attempted': None,
            'takedowns_landed': None,
            'ufc_debut': None,
            'weight': None,
            'win_by_dec_amount': None,
            'win_by_ko_tko_amount': None,
            'win_by_sub_amount': None,
            'wins_by_knockout': None,
            'trains_at': None,
            'place_of_birth': None,
            'status': None,
            'fight_style': None,
            # Add other optional fields here
        }
        for field, default_value in optional_fields.items():
            stats[field] = stats.get(field, default_value)

        for field in stats.keys():
            if field not in allowed_attributes:
                return jsonify({'error': f'Invalid field: {field}'}), 400

        conn = connect_db()
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
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
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
        cursor.execute("SELECT currval(pg_get_serial_sequence('fighters', 'id'))")
        fighter_id = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return jsonify({'message': 'Fighter created successfully', 'fighter_id': fighter_id}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/fighters/<int:fighter_id>', methods=['PUT'])
def update_fighter(fighter_id):
    try:
        data = request.json
        # Validate input fields
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # Construct the SET part of the SQL query dynamically based on the provided data
        set_values = []
        set_params = []
        for key, value in data.items():
            # Only update if the key is valid and not the fighter_id
            if key in ['name', 'division_title', 'win', 'loss', 'draw', 'trains_at', 'place_of_birth',
                       'status', 'fight_style', 'age', 'height', 'weight', 'ufc_debut', 'reach', 'leg_reach',
                       'wins_by_knockout', 'first_round_finishes', 'striking_accuracy_percent',
                       'significant_strikes_landed', 'significant_strikes_attempted',
                       'takedown_accuracy_percent', 'takedowns_landed', 'takedowns_attempted',
                       'sig_str_landed_per_min', 'sig_str_absorbed_per_min', 'takedown_avg_per_15_min',
                       'submission_avg_per_15_min', 'sig_str_defense_percent', 'takedown_defense_percent',
                       'knockdown_avg', 'average_fight_time', 'sig_str_standing_amount', 'sig_str_clinch_amount',
                       'sig_str_ground_amount', 'win_by_ko_tko_amount', 'win_by_dec_amount', 'win_by_sub_amount',
                       'sig_str_standing_percentage', 'sig_str_clinch_percentage', 'sig_str_ground_percentage',
                       'strike_to_head', 'strike_to_head_per', 'strike_to_body', 'strike_to_body_per', 'strike_to_leg',
                       'strike_to_leg_per']:
                set_values.append(f"{key} = %s")
                set_params.append(value)

        # Check if any valid fields were provided for update
        if not set_values:
            return jsonify({'error': 'No valid fields provided for update'}), 400

        # Add fighter_id to the parameters list
        set_params.append(fighter_id)

        # Construct the UPDATE query
        update_query = f"""
            UPDATE fighters
            SET {', '.join(set_values)}
            WHERE id = %s
        """

        conn = connect_db()
        with conn.cursor() as cur:
            cur.execute(update_query, set_params)
            if cur.rowcount == 0:
                return jsonify({'error': 'Fighter not found'}), 404
            conn.commit()
        conn.close()

        return jsonify({'message': 'Fighter updated successfully'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/fighters/<int:fighter_id>', methods=['DELETE'])
def delete_fighter(fighter_id):
    try:
        conn = connect_db()
        with conn.cursor() as cur:
            cur.execute("DELETE FROM fighters WHERE id = %s", (fighter_id,))
            if cur.rowcount == 0:
                conn.rollback()  # Rollback the transaction if no rows were deleted
                return jsonify({'error': 'Fighter not found'}), 404

            # Update the primary key sequence to prevent gaps
            cur.execute("SELECT setval(pg_get_serial_sequence('fighters', 'id'), coalesce(max(id),0)) FROM fighters")
            conn.commit()

        conn.close()
        return jsonify({'message': 'Fighter deleted successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
