from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Replace with your MySQL database configuration
db = mysql.connector.connect(
    host="localhost",
    user="yourusername",
    password="yourpassword",
    database="yourdatabase"
)
cursor = db.cursor()

@app.route('/book', methods=['POST'])
def book():
    try:
        # Get form data
        name = request.form.get('name')
        user_email = request.form.get('user_email')
        appointment_date = request.form.get('appointment_date')
        appointment_time = request.form.get('appointment_time')

        # Validate required fields
        if not (name and user_email and appointment_date and appointment_time):
            return jsonify({'error': 'Missing required fields'}), 400

        # Insert into database
        sql = "INSERT INTO appointments (user_name, user_email, appointment_date, appointment_time) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (name, user_email, appointment_date, appointment_time))
        db.commit()  # Commit changes to the database

        return jsonify({'message': 'Appointment booked successfully!'})

    except mysql.connector.Error as err:
        db.rollback()  # Rollback changes in case of error
        return jsonify({'error': f'Database error: {str(err)}'}), 500

    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
