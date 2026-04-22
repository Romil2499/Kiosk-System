import sqlite3

def create_database():
    # This creates a file named 'kiosk_data.db' in your folder
    conn = sqlite3.connect('kiosk_data.db')
    cursor = conn.cursor()

    # --- TABLE 1: Information (FAQs) ---
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS faqs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            question TEXT NOT NULL,
            answer TEXT NOT NULL
        )
    ''')

    # --- TABLE 2: Ticketing (Queue) ---
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS queue_tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_number TEXT NOT NULL,
            department TEXT NOT NULL,
            queue_number INTEGER NOT NULL,
            status TEXT DEFAULT 'Waiting',
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # --- INSERT SEED DATA (Dummy Info for Testing) ---
    # We clear the table first just in case you run this file twice
    cursor.execute('DELETE FROM faqs')
    
    # Adding some sample ICCT information that the admin can edit later
    sample_faqs = [
        ("Enrollment", "When is the enrollment for next semester?", "Enrollment for the 1st Trimester starts on August 15. Please bring your clearance."),
        ("Tuition", "How much is the tuition fee for BSIT?", "The estimated tuition fee for BSIT is ₱18,000 per trimester, depending on your units."),
        ("Requirements", "What are the requirements for Freshmen?", "Please bring your Form 138, Good Moral Certificate, PSA Birth Certificate, and 2x2 pictures.")
    ]
    
    cursor.executemany('''
        INSERT INTO faqs (category, question, answer) 
        VALUES (?, ?, ?)
    ''', sample_faqs)

    # Save changes and close
    conn.commit()
    conn.close()
    print("Database 'kiosk_data.db' created successfully with sample FAQs!")

if __name__ == '__main__':
    create_database()