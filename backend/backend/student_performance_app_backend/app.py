import os
import numpy as np
from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_session import Session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import joblib

app = Flask(__name__)
CORS(app, supports_credentials=True)

app.secret_key = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'binki123'
app.config['MYSQL_DB'] = 'student_app'

mysql = MySQL(app)

model = joblib.load(r'C:\Users\User\AppData\Local\Programs\Python\Python313\student_performance_app\backend\student_performance_app_backend\model\student_model.pkl')
print("Model loaded successfully.")

@app.route('/')
def index():
    return 'Flask + MySQL + ML Backend Running!'

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not all([name, email, password]):
        return jsonify({'success': False, 'message': 'Missing fields'}), 400

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    existing_user = cur.fetchone()
    if existing_user:
        return jsonify({'success': False, 'message': 'Email already exists'}), 409

    hashed_password = generate_password_hash(password)
    try:
        cur.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                    (name, email, hashed_password))
        mysql.connection.commit()
        return jsonify({'success': True, 'message': 'User registered successfully'}), 201
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not all([email, password]):
        return jsonify({"success": False, "message": "Missing credentials"}), 400

    cur = mysql.connection.cursor()
    cur.execute("SELECT id, name, email, password FROM users WHERE email = %s", (email,))
    user = cur.fetchone()

    if user and check_password_hash(user[3], password):
        session['user_id'] = user[0]
        return jsonify({
            "success": True,
            "message": "Login successful",
            "user": {
                "id": user[0],
                "name": user[1],
                "email": user[2]
            }
        }), 200
    else:
        return jsonify({"success": False, "message": "Invalid credentials"}), 401

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"message": "Logout successful"}), 200

@app.route('/predict-performance', methods=['POST'])
def predict_performance():
    if 'user_id' not in session:
        return jsonify({"error": "You must be logged in"}), 401

    data = request.get_json()
    try:
        features = [
            data['gender'], data['ethnicity'], data['parental_level_of_education'],
            data['lunch'], data['test_preparation_course'], data['math_score'],
            data['reading_score'], data['writing_score']
        ]
        features_array = np.array(features).reshape(1, -1)
        prediction = model.predict(features_array)[0]
        return jsonify({'prediction': int(prediction)})
    except KeyError:
        return jsonify({'error': 'Missing one or more required fields'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generate-schedule', methods=['POST'])
def generate_schedule():
    if 'user_id' not in session:
        return jsonify({"error": "You must be logged in"}), 401

    data = request.get_json()
    user_id = session['user_id']
    schedule = data.get('schedule')

    if not schedule:
        return jsonify({'error': 'Schedule data is required'}), 400

    try:
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM schedules WHERE user_id = %s", (user_id,))

        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        for i, task in enumerate(schedule):
            day = days[i % 7]
            cursor.execute('''
                INSERT INTO schedules (user_id, day, subject, hours)
                VALUES (%s, %s, %s, %s)
            ''', (user_id, day, task['subject'], task['hours']))

        mysql.connection.commit()
        return jsonify({'message': 'Schedule generated and saved successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Registered routes:", app.url_map)
    app.run(debug=True)

