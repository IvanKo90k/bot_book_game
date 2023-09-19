import sqlite3
import time
import os


# def create_table_id():
#     connect = sqlite3.connect('Data/clients_id.db')
#     cursor = connect.cursor()
#     cursor.execute('CREATE TABLE IF NOT EXISTS clients_id (userid INTEGER, username TEXT)')
#     connect.commit()
#     cursor.close()
# 'CREATE TABLE users (userid INTEGER, username TEXT, data DATETIME DEFAULT CURRENT_TIMESTAMP)'


def create_table():
    connect = sqlite3.connect('Data/table_with_words.db')
    cursor = connect.cursor()
    cursor.execute(
        f'CREATE TABLE IF NOT EXISTS table_with_words (word_id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, eng_word TEXT, ua_word TEXT, transcription TEXT, date INTEGER, check_date INTEGER, level INTEGER, score INTEGER, column1 TEXT, column2 TEXT)')
    connect.commit()
    cursor.close()


def insert_7_values(user_id, eng_word, ua_word, transcription, date, check_date, level):
    connect = sqlite3.connect('Data/table_with_words.db')
    cursor = connect.cursor()
    cursor.execute(
        'INSERT INTO table_with_words (user_id, eng_word, ua_word, transcription, date, check_date, level) VALUES (?, ?, ?, ?, ?, ?, ?)',
        (user_id, eng_word, ua_word, transcription, date, check_date, level))
    connect.commit()
    cursor.close()


def insert_word_id(word_id):
    connect = sqlite3.connect('Data/table_with_words.db')
    cursor = connect.cursor()
    cursor.execute('INSERT INTO table_with_words (word_id) VALUES (?)', (word_id,))
    connect.commit()
    cursor.close()


def insert_user_0(user_id):
    connect = sqlite3.connect('Data/table_with_words.db')
    cursor = connect.cursor()
    cursor.execute('INSERT INTO table_with_words (user_id) VALUES (?)', (user_id,))
    connect.commit()
    cursor.close()


def insert_user(user_id, word_id):
    connect = sqlite3.connect('Data/table_with_words.db')
    cursor = connect.cursor()
    cursor.execute('INSERT INTO table_with_words (word_id, user_id) VALUES (?, ?)', (word_id, user_id))
    connect.commit()
    cursor.close()


def insert_user_eng_words(eng_word):
    connect = sqlite3.connect('Data/table_with_words.db')
    cursor = connect.cursor()
    cursor.execute('INSERT INTO table_with_words (eng_word) VALUES (?)', (eng_word,))
    connect.commit()
    cursor.close()


def insert_usersid():
    connect = sqlite3.connect('Data/test.db')
    cursor = connect.cursor()
    cursor.execute('INSERT INTO users (userid) VALUES (2143)')
    connect.commit()
    cursor.close()


def update_eng_word(eng_word, transcription, word_id):
    connect = sqlite3.connect('Data/table_with_words.db')
    cursor = connect.cursor()
    cursor.execute(f'UPDATE table_with_words SET eng_word="{eng_word}" WHERE word_id={word_id}')
    cursor.execute(f'UPDATE table_with_words SET transcription="{transcription}" WHERE word_id={word_id}')
    connect.commit()
    cursor.close()


def update(word_id, ua_word, date, check_date, level):
    connect = sqlite3.connect('Data/table_with_words.db')
    cursor = connect.cursor()
    cursor.execute(f'UPDATE table_with_words SET ua_word="{ua_word}" WHERE word_id={word_id}')
    cursor.execute(f'UPDATE table_with_words SET date="{date}" WHERE word_id={word_id}')
    cursor.execute(f'UPDATE table_with_words SET check_date="{check_date}" WHERE word_id={word_id}')
    cursor.execute(f'UPDATE table_with_words SET level="{level}" WHERE word_id={word_id}')
    connect.commit()
    cursor.close()


def update_one_value(word_id, column_name, value):
    print(f"word_id: {word_id}, column_name: {column_name}, value: {value} - update_one_value/DB")  # Add this line
    connect = sqlite3.connect('Data/table_with_words.db')
    cursor = connect.cursor()
    cursor.execute(f'UPDATE table_with_words SET {column_name}="{value}" WHERE word_id={word_id}')
    connect.commit()
    cursor.close()


def update_date_lvl(word_id, date, level):
    connect = sqlite3.connect('Data/table_with_words.db')
    cursor = connect.cursor()
    cursor.execute(f'UPDATE table_with_words SET date="{date}" WHERE word_id={word_id}')
    cursor.execute(f'UPDATE table_with_words SET level="{level}" WHERE word_id={word_id}')
    connect.commit()
    cursor.close()


def get_all_values():
    connect = sqlite3.connect('Data/table_with_words.db')
    cursor = connect.cursor()
    cursor.execute('SELECT * FROM table_with_words')
    res = cursor.fetchall()
    print(res)
    cursor.close()


def get_one_row(number):
    connect = sqlite3.connect('Data/table_with_words.db')
    cursor = connect.cursor()
    cursor.execute(f'SELECT * FROM table_with_words LIMIT 1 OFFSET {number - 1}')
    res = list(cursor.fetchone())
    cursor.close()
    return res



def get_unique_values(column_name):
    # Connect to the SQLite database
    conn = sqlite3.connect('Data/table_with_words.db')
    cursor = conn.cursor()

    # Execute a query to retrieve unique values from the specified column
    # column_name = 'user_id'
    query = f"SELECT DISTINCT {column_name} FROM table_with_words"
    cursor.execute(query)

    # Fetch all the unique values
    unique_values = cursor.fetchall()

    # Close the database connection
    conn.close()

    # Convert the fetched values to a list
    unique_values_list = [value[0] for value in unique_values]

    # Print the list of unique values
    print(unique_values_list)
    return unique_values_list


def create_database_if_not_exists():
    db_file = 'Data/table_with_words.db'

    # Check if the database file exists
    if not os.path.exists(db_file):
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Define the SQL statement to create the table
        create_table_sql = '''
        CREATE TABLE IF NOT EXISTS table_with_words (
            word_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            eng_word TEXT,
            ua_word TEXT,
            transcription TEXT,
            date INTEGER,
            check_date INTEGER,
            level INTEGER,
            score INTEGER,
            column1 TEXT, 
            column2 TEXT
        );
        '''

        # Execute the SQL statement to create the table
        cursor.execute(create_table_sql)

        # Commit the changes and close the database connection
        conn.commit()
        conn.close()


def get_values_if_conditions(column_name_1, column_name_2):
    # Call the function to create the database and table if they don't exist
    create_database_if_not_exists()

    # Continue with your existing code to retrieve data from the database
    db_file = 'Data/table_with_words.db'
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    threshold_date = time.time()
    print(threshold_date, 'get_values_if_conditions на DB')

    query = f"SELECT DISTINCT {column_name_1} FROM table_with_words WHERE {column_name_2} < ?"
    cursor.execute(query, (threshold_date,))
    results = cursor.fetchall()

    conn.close()

    user_id_list = [user_id[0] for user_id in results]

    print(user_id_list, 'get_values_if_conditions/DB.py')
    return user_id_list


# def get_values_if_conditions(column_name_1, column_name_2):
#     # Connect to the SQLite database
#     conn = sqlite3.connect('Data/table_with_words.db')
#     cursor = conn.cursor()
#
#     # Specify the threshold date
#     threshold_date = time.time()
#     print(threshold_date, 'get_values_if_conditions на DB')
#
#     # # Execute a query to retrieve the "user_id" values where "check_date" is less than the threshold
#     query = f"SELECT DISTINCT {column_name_1} FROM table_with_words WHERE {column_name_2} < ?"
#     cursor.execute(query, (threshold_date,))
#
#     # Fetch all the results
#     results = cursor.fetchall()
#
#     # Close the database connection
#     conn.close()
#
#     # Convert the fetched values to a list
#     user_id_list = [user_id[0] for user_id in results]
#
#     # Print the list of "user_id" values
#     print(user_id_list)
#     return user_id_list


def get_username0(userid):
    connect = sqlite3.connect('Data/test.db')
    cursor = connect.cursor()
    cursor.execute(f'SELECT username FROM users WHERE userid={userid}')
    res = cursor.fetchall()
    print(res)
    cursor.close()


def get_username(user_id):
    connect = sqlite3.connect('Data/table_with_words.db')
    cursor = connect.cursor()
    cursor.execute(f'SELECT user_id FROM table_with_words WHERE user_id=?', (user_id,))
    res = cursor.fetchall()
    cursor.close()
    try:
        t = res[0]
        return True
    except:
        return False


def get_one_value(date, column_name, user_id):
    connect = sqlite3.connect('Data/table_with_words.db')
    cursor = connect.cursor()
    cursor.execute(f'SELECT {date} FROM table_with_words WHERE {column_name}=?', (user_id,))
    res = cursor.fetchall()
    cursor.close()


def get_value_universal(level, user_id, word_id):
    connect = sqlite3.connect('Data/clients_id.db')
    cursor = connect.cursor()
    cursor.execute(f'SELECT {level} FROM table_with_words WHERE {user_id}=?', (word_id,))
    res = cursor.fetchall()
    cursor.close()


def get_username2(userid):
    connect = sqlite3.connect('Data/clients_id.db')
    cursor = connect.cursor()
    cursor.execute(f'SELECT userid FROM clients_id WHERE userid=?', (userid,))
    res = cursor.fetchall()
    print(res)
    cursor.close()


def count_rows_in_database():
    # Connect to the database
    connect = sqlite3.connect('Data/table_with_words.db')

    # Create a cursor object to execute SQL queries
    cursor = connect.cursor()

    # Execute the query to count the rows
    cursor.execute(f'SELECT COUNT(*) FROM table_with_words')

    # Fetch the result of the query
    row_count = cursor.fetchone()[0]

    # Close the cursor and the database connection
    cursor.close()
    connect.close()

    # Return the row count
    return row_count


def count_rows_with_value(value):
    # Connect to the database
    conn = sqlite3.connect('Data/table_with_words.db')

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Execute the SELECT COUNT(*) query
    cursor.execute(f"SELECT COUNT(*) FROM table_with_words WHERE user_id = ?", (value,))

    # Fetch the result row
    count = cursor.fetchone()[0]
    # print(value)

    # Close the cursor and the database connection
    cursor.close()
    conn.close()

    # Return the count of rows with the specified value
    return count


def check_row_with_two_values(column1_name, column1_value, column2_name, column2_value):
    # Connect to the database
    conn = sqlite3.connect('Data/table_with_words.db')

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Execute the SELECT COUNT(*) query
    cursor.execute(f"SELECT COUNT(*) FROM table_with_words WHERE {column1_name} = ? AND {column2_name} = ?",
                   (column1_value, column2_value))

    # Fetch the result row
    count = cursor.fetchone()[0]

    # Close the cursor and the database connection
    cursor.close()
    conn.close()
    print(f'Перевірка наявності слова в таблиці SQL: {count > 0} (check_row_with_two_values на DB)')

    # Return True if a row exists with the specified values, otherwise False
    return count > 0


def delete_row_with_empty_cell(column_name):
    # Connect to the database
    conn = sqlite3.connect('Data/table_with_words.db')

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Execute the DELETE query to remove rows with empty cells
    cursor.execute(f"DELETE FROM table_with_words WHERE {column_name} IS NULL OR {column_name} = ''")

    # Commit the transaction to save the changes
    conn.commit()

    # Close the cursor and the database connection
    cursor.close()
    conn.close()
