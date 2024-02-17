import sqlite3
import time
import os

def create_database_if_not_exists():
    db_file = 'Data/table_with_data.db'

    # Check if the database file exists
    if not os.path.exists(db_file):
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Define the SQL statement to create the table
        create_table_sql = '''
        CREATE TABLE IF NOT EXISTS table_with_data (
            word_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            Mastery INTEGER,
            Endurance INTEGER,
            Luck INTEGER,
            column1 INTEGER,
            column2 TEXT,
            column3 TEXT
        );
        '''

        # Execute the SQL statement to create the table
        cursor.execute(create_table_sql)

        # Commit the changes and close the database connection
        conn.commit()
        conn.close()
def retrieve_character_data(user_id):
    create_database_if_not_exists()
    db_file = 'Data/table_with_data.db'
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Retrieve character data from the database
    cursor.execute("SELECT Mastery, Endurance, Luck FROM table_with_data WHERE user_id = ?", (user_id,))
    data = cursor.fetchone()

    conn.close()

    print("User ID:", user_id)
    print("Retrieved Data:", data)

    return data

retrieve_character_data(560101130)
