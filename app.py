from flask import Flask, render_template, jsonify, request
import sqlite3
from datetime import datetime

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('kiosk_data.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('index.html')
# --- NEW: The Admin Dashboard Route ---
@app.route('/admin')
def admin_dashboard():
    # In a real scenario, this would query vz SQLite database to get the real numbers
    current_ticket = 5
    waiting_count = 3
    return render_template('admin.html', current=current_ticket, waiting=waiting_count)

@app.route('/api/faqs')
def get_faqs():
    conn = get_db_connection()
    faqs = conn.execute('SELECT * FROM faqs').fetchall()
    conn.close()
    faq_list = [{'id': row['id'], 'category': row['category'], 'question': row['question'], 'answer': row['answer']} for row in faqs]
    return jsonify(faq_list)

# --- NEW: The Ticketing Logic ---
@app.route('/api/ticket', methods=['POST'])
def generate_ticket():
    data = request.get_json()
    student_number = data.get('student_number')
    department = data.get('department')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Count how many people are currently waiting for this department to calculate the queue number
    cursor.execute('SELECT COUNT(*) FROM queue_tickets WHERE department = ? AND status = "Waiting"', (department,))
    current_queue_count = cursor.fetchone()[0]
    new_queue_number = current_queue_count + 1
    
    # Save the new ticket to the database
    cursor.execute('''
        INSERT INTO queue_tickets (student_number, department, queue_number, status)
        VALUES (?, ?, ?, "Waiting")
    ''', (student_number, department, new_queue_number))
    
    conn.commit()
    conn.close()
    
    # Send the ticket details back to the frontend
    return jsonify({
        'queue_number': new_queue_number,
        'department': department,
        'student_number': student_number,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
# --- NEW: The Admin Settings Route (For changing FAQs) ---
@app.route('/admin/settings', methods=['GET', 'POST'])
def admin_settings():
    conn = get_db_connection()
    
    # If the admin clicked "Save Updates", update the database
    if request.method == 'POST':
        # Loop through whatever they typed in the form
        for key, new_answer in request.form.items():
            if key.startswith('faq_'):
                # Extract the ID number of the question
                faq_id = key.split('_')[1]
                # Update the database with the new text
                conn.execute('UPDATE faqs SET answer = ? WHERE id = ?', (new_answer, faq_id))
        
        conn.commit()
        # You can add a success message here later

    # Get the current FAQs to display on the screen
    faqs = conn.execute('SELECT * FROM faqs').fetchall()
    conn.close()
    
    return render_template('admin_settings.html', faqs=faqs)
if __name__ == '__main__':
    app.run(debug=True, port=5000)