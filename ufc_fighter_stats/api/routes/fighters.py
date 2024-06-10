from flask import Blueprint, jsonify, request
import psycopg2
from psycopg2.extras import RealDictCursor

bp = Blueprint('fighters', __name__, url_prefix='/api/fighters')

db_config = {
    'dbname': 'ufc_fighter_stats',
    'user': 'postgres',
    'password': '1234',
    'host': 'localhost'
}

#connect to database
def connect_db():
    conn = psycopg2.cpnnect(**db_config)
    return conn

@bp.route('/api/fighters', methods=['GET'])
def get_fighters():
    conn = connect_db()
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT * FROM fighters")
        fighters = cur.fetchall()
    conn.close()
    return jsonify(fighters)

@bp.route('/api/fighters/<int:fighter_id>', methods=['GET'])
def get_fighter(fighter_id):
    conn = connect_db()
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT * FROM fighters WHERE id = %s", (fighter_id,))
        fighter = cur.fetchone()
        if fighter is None:
            return jsonify({'error': 'Fighter not found'}), 404
    conn.close()
    return jsonify(fighter)

@bp.route('/api/fighters', methods=['POST'])
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

@bp.route('/api/fighters/<int:fighter_id>', methods=['PUT'])
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

@bp.route('/api/fighters/<int:fighter_id>', methods=['DELETE'])
def delete_fighter(fighter_id):
    conn = connect_db()
    with conn.cursor() as cur:
        cur.execute("DELETE FROM fighters WHERE id = %s", (fighter_id,))
        if cur.rowcount == 0:
            return jsonify({'error': 'Fighter not found'}), 404
        conn.commit()
    conn.close()
    return jsonify({'message': 'Fighter deleted successfully'})