from flask import Flask, jsonify, request
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
db_config = {
    'dbname': 'ufc_fighter_data',
    'user': 'postgres',
    'password': '1234',
    'host': 'localhost'
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
    return "Hello World"

"""
@app.route('/api/test')
def test_db_connection():
    # Attempt to connect to the database
    conn = connect_db()
    if conn:
        try:
            # Example query: Retrieve all records from a table
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM your_table")
            records = cursor.fetchall()
            cursor.close()
            conn.close()
            return jsonify(records)
        except psycopg2.Error as e:
            # Handle query errors
            print("Database query error:", e)
            return jsonify({'error': 'Database query error'})
    else:
        return jsonify({'error': 'Failed to connect to the database'})
"""


@app.route('/api/fighters', methods=['GET'])
def get_fighters():
    conn = connect_db()
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT * FROM fighters ORDER BY id")
        fighters = cur.fetchall()
    conn.close()
    return jsonify(fighters)

@app.route('/api/fighters/<int:fighter_id>', methods=['GET'])
def get_fighter(fighter_id):
    conn = connect_db()
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT * FROM fighters WHERE id = %s", (fighter_id,))
        fighter = cur.fetchone()
        if fighter is None:
            return jsonify({'error': 'Fighter not found'}), 404
    conn.close()
    return jsonify(fighter)

@app.route('/api/fighters/<string:name>', methods=['GET'])
def get_fighter_by_name(name):
    conn = connect_db()
    if not conn:
        return jsonify({'error': 'Failed to connect to the database'}), 500
    
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT * FROM fighters WHERE name = %s", (name,))
        fighter = cur.fetchone()
        if fighter is None:
            return jsonify({'error': 'Fighter not found'}), 404
    
    conn.close()
    return jsonify(fighter)

@app.route('/api/fighters', methods=['POST'])
def create_fighter():
    data = request.json
    # Validate input fields
    required_fields = ['name', 'division_title', 'win', 'loss', 'draw']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    conn = connect_db()
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO fighters (name, division_title, win, loss, draw)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        """, (data['name'], data['division_title'], data['win'], data['loss'], data['draw']))
        fighter_id = cur.fetchone()[0]
        conn.commit()
    conn.close()
    return jsonify({'message': 'Fighter created successfully', 'fighter_id': fighter_id}), 201

@app.route('/api/fighters/<int:fighter_id>', methods=['PUT'])
def update_fighter(fighter_id):
    data = request.json
    # Validate input fields
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    conn = connect_db()
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE fighters
            SET name = %s, division_title = %s, win = %s, loss = %s, draw = %s
            WHERE id = %s
        """, (data.get('name'), data.get('division_title'), data.get('win'), data.get('loss'), data.get('draw'), fighter_id))
        if cur.rowcount == 0:
            return jsonify({'error': 'Fighter not found'}), 404
        conn.commit()
    conn.close()
    return jsonify({'message': 'Fighter updated successfully'})

@app.route('/api/fighters/<int:fighter_id>', methods=['DELETE'])
def delete_fighter(fighter_id):
    conn = connect_db()
    with conn.cursor() as cur:
        cur.execute("DELETE FROM fighters WHERE id = %s", (fighter_id,))
        if cur.rowcount == 0:
            return jsonify({'error': 'Fighter not found'}), 404
        conn.commit()
    conn.close()
    return jsonify({'message': 'Fighter deleted successfully'})