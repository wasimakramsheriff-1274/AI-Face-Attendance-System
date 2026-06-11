from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def fetch_attendance_logs():
    """Safely connects to the database and pulls log rows ordered from newest to oldest."""
    try:
        conn = sqlite3.connect('attendance.db')
        cursor = conn.cursor()
        # Fetch records descending so the latest scans show at the very top
        cursor.execute("SELECT id, name, date, time FROM logs ORDER BY id DESC")
        rows = cursor.fetchall()
        conn.close()
        return rows
    except Exception as e:
        print(f"Database error: {e}")
        return []

@app.route('/')
def home():
    logs = fetch_attendance_logs()
    
    # Calculate quick dashboard analytics metrics
    total_scans = len(logs)
    unique_attendees = len(set([row[1] for row in logs]))
    
    return render_template('dashboard.html', logs=logs, total_scans=total_scans, unique_users=unique_attendees)

if __name__ == '__main__':
    # Start server locally on port 5000
    app.run(debug=True, port=5000)