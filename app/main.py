import logging
import os
from flask import Flask, request, render_template, jsonify
from dotenv import load_dotenv
from db import DatabaseManager

load_dotenv()

app = Flask(__name__)

db = DatabaseManager(
    name=os.getenv("PG_DB_NAME"),
    user=os.getenv("PG_ADMIN"),
    password=os.getenv("PG_ADMIN_PASS"),
    host=os.getenv("PG_HOST", "localhost")
)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_messages', methods=['GET'])
def get_messages():
    try:
        r = db.get_messages()
        return jsonify({'success': True, 'status': r})
    except Exception as e:
        logging.error(e)
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/add_message', methods=['POST'])
def add_message():
    data = request.get_json()
    text = data.get('text')
    username = data.get('username')

    if not text or not username:
        return jsonify({'success': False, 'error': 'Missing text or username'}), 400

    try:
        if db.add_message(text, username):
            return jsonify({'success': True, 'status': 'Message added successfully'})
        else:
            return jsonify({'success': False, 'error': 'Failed to add message'}), 500
    except Exception as e:
        logging.error(e)
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    db.connect()
    db.init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
