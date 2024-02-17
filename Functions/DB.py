import sqlite3
import time
import os


# def create_table():
#     connect = sqlite3.connect('Data/table_with_data.db')
#     cursor = connect.cursor()
#     cursor.execute(
#         f'CREATE TABLE IF NOT EXISTS table_with_data (word_id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, Mastery INTEGER, Endurance INTEGER, Luck INTEGER, text_number INTEGER, money INTEGER, e_mastery_2 INTEGER, e_endurance_2 INTEGER, e_mastery_3 INTEGER, e_endurance_3 INTEGER, e_mastery_4 INTEGER, e_endurance_4 INTEGER, food_briquette INTEGER, e_mastery_17 INTEGER, e_endurance_17 INTEGER, e_mastery_24_1 INTEGER, e_endurance_24_1 INTEGER, e_mastery_24_2 INTEGER, e_endurance_24_2 INTEGER, flag24 INTEGER, e_mastery_35 INTEGER, e_endurance_35 INTEGER, rope382 INTEGER, scaner110_117_381 INTEGER, sword INTEGER, rat_bite INTEGER, e_mastery_55 INTEGER, e_endurance_55 INTEGER, e_mastery_82 INTEGER, e_endurance_82 INTEGER, e_mastery_84 INTEGER, e_endurance_84 INTEGER, e_mastery_104 INTEGER, e_endurance_104 INTEGER, e_mastery_106 INTEGER, e_endurance_106 INTEGER, e_mastery_107 INTEGER, e_endurance_107 INTEGER, dogfight_107 INTEGER, e_mastery_113_1 INTEGER, e_endurance_113_1 INTEGER, e_mastery_113_2 INTEGER, e_endurance_113_2 INTEGER, flag113 INTEGER, e_mastery_124 INTEGER, e_endurance_124 INTEGER, column22 INTEGER, column23 INTEGER, column24 INTEGER, money382 INTEGER))')
#     connect.commit()
#     cursor.close()

def create_table():
    table_query = '''
    CREATE TABLE IF NOT EXISTS table_with_data (
        word_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        Mastery INTEGER,
        Endurance INTEGER,
        Luck INTEGER,
        max_mastery INTEGER,
        max_endurance INTEGER,
        max_luck INTEGER,
        text_number INTEGER,
        money INTEGER,
        e_mastery_2 INTEGER,
        e_endurance_2 INTEGER,
        e_mastery_3 INTEGER,
        e_endurance_3 INTEGER,
        e_mastery_4 INTEGER,
        e_endurance_4 INTEGER,
        food_briquette_12 INTEGER,
        e_mastery_17 INTEGER,
        e_endurance_17 INTEGER,
        e_mastery_24_1 INTEGER,
        e_endurance_24_1 INTEGER,
        e_mastery_24_2 INTEGER,
        e_endurance_24_2 INTEGER,
        flag24 INTEGER,
        e_mastery_35 INTEGER,
        e_endurance_35 INTEGER,
        zodiac_47 INTEGER,
        sword INTEGER,
        rat_bite INTEGER,
        e_mastery_55 INTEGER,
        e_endurance_55 INTEGER,
        appointment_74 INTEGER,
        e_mastery_82 INTEGER,
        e_endurance_82 INTEGER,
        e_mastery_84 INTEGER,
        e_endurance_84 INTEGER,
        e_mastery_104 INTEGER,
        e_endurance_104 INTEGER,
        e_mastery_106 INTEGER,
        e_endurance_106 INTEGER,
        e_mastery_107 INTEGER,
        e_endurance_107 INTEGER,
        dogfight_107 INTEGER,
        sealed_tube_110 INTEGER,
        magnetic_mine_110 INTEGER,
        grenade_110_215 INTEGER,
        hand_phaser_110 INTEGER,
        scanner_110_117 INTEGER,
        buttons_data_110 TEXT,
        e_mastery_113_1 INTEGER,
        e_endurance_113_1 INTEGER,
        e_mastery_113_2 INTEGER,
        e_endurance_113_2 INTEGER,
        flag113 INTEGER,
        bracelet_ziridium_117 INTEGER,
        e_mastery_124 INTEGER,
        e_endurance_124 INTEGER,
        e_mastery_133 INTEGER,
        e_endurance_133 INTEGER,
        e_mastery_136 INTEGER,
        e_endurance_136 INTEGER,
        killed_145 INTEGER,
        e_mastery_150 INTEGER,
        e_endurance_150 INTEGER,
        check_152 INTEGER,
        uniform_155 INTEGER,
        e_mastery_157 INTEGER,
        e_endurance_157 INTEGER,
        e_mastery_161 INTEGER,
        e_endurance_161 INTEGER,
        e_mastery_165 INTEGER,
        e_endurance_165 INTEGER,
        button_172 INTEGER,
        e_mastery_172_1 INTEGER,
        e_endurance_172_1 INTEGER,
        e_mastery_172_2 INTEGER,
        e_endurance_172_2 INTEGER,
        flag172 INTEGER,
        e_mastery_179 INTEGER,
        e_endurance_179 INTEGER,
        e_mastery_190 INTEGER,
        e_endurance_190 INTEGER,
        flag190 INTEGER,
        flag190_2 INTEGER,
        attack_190 INTEGER,
        e_mastery_206 INTEGER,
        e_endurance_206 INTEGER,
        e_mastery_215 INTEGER,
        e_endurance_215 INTEGER,
        e_mastery_224 INTEGER,
        e_endurance_224 INTEGER,
        without_weapons INTEGER,
        e_mastery_234_1 INTEGER,
        e_endurance_234_1 INTEGER,
        e_mastery_234_2 INTEGER,
        e_endurance_234_2 INTEGER,
        flag234 INTEGER,
        number_238 INTEGER,
        e_mastery_243 INTEGER,
        e_endurance_243 INTEGER,
        sand243 INTEGER,
        rounds243 INTEGER,
        e_mastery_244_1 INTEGER,
        e_endurance_244_1 INTEGER,
        e_mastery_244_2 INTEGER,
        e_endurance_244_2 INTEGER,
        flag244 INTEGER,
        jetpack_253 INTEGER,
        p_366_or_295 INTEGER,
        e_mastery_289 INTEGER,
        e_endurance_289 INTEGER,
        column22 INTEGER,
        column23 INTEGER,
        column24 INTEGER,
        e_mastery_295 INTEGER,
        e_endurance_295 INTEGER,
        e_mastery_295_1 INTEGER,
        e_endurance_295_1 INTEGER,
        e_mastery_295_2 INTEGER,
        e_endurance_295_2 INTEGER,
        e_mastery_295_3 INTEGER,
        e_endurance_295_3 INTEGER,
        e_mastery_295_4 INTEGER,
        e_endurance_295_4 INTEGER,
        flag295 INTEGER,
        e_mastery_298 INTEGER,
        e_endurance_298 INTEGER,
        e_mastery_313 INTEGER,
        e_endurance_313 INTEGER,
        e_mastery_341 INTEGER,
        e_endurance_341 INTEGER,
        e_mastery_351 INTEGER,
        e_endurance_351 INTEGER,
        warder_355 INTEGER,
        brain_probe_355 INTEGER,
        buttons_data_355 TEXT,
        e_mastery_366 INTEGER,
        e_endurance_366 INTEGER,
        e_mastery_366_1 INTEGER,
        e_endurance_366_1 INTEGER,
        e_mastery_366_2 INTEGER,
        e_endurance_366_2 INTEGER,
        e_mastery_366_3 INTEGER,
        e_endurance_366_3 INTEGER,
        e_mastery_366_4 INTEGER,
        e_endurance_366_4 INTEGER,
        flag366 INTEGER,
        e_mastery_367 INTEGER,
        e_endurance_367 INTEGER,
        e_mastery_373 INTEGER,
        e_endurance_373 INTEGER,
        e_mastery_373_1 INTEGER,
        e_endurance_373_1 INTEGER,
        e_mastery_373_2 INTEGER,
        e_endurance_373_2 INTEGER,
        e_mastery_375 INTEGER,
        e_endurance_375 INTEGER,
        money382 INTEGER,
        stroboscope_382 INTEGER,
        manual_horn_382 INTEGER,
        skein_of_nylon_rope_382 INTEGER,
        can_of_motor_oil_382 INTEGER,
        personal_robot_382 INTEGER,
        buttons_data_382 TEXT,
        e_mastery_391 INTEGER,
        e_endurance_391 INTEGER,
        cutter393 INTEGER
    )
    '''

    connect = sqlite3.connect('Data/table_with_data.db')
    cursor = connect.cursor()
    cursor.execute(table_query)
    connect.commit()
    cursor.close()


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
            max_mastery INTEGER,
            max_endurance INTEGER,
            max_luck INTEGER,
            text_number INTEGER,
            money INTEGER,
            e_mastery_2 INTEGER,
            e_endurance_2 INTEGER,
            e_mastery_3 INTEGER,
            e_endurance_3 INTEGER,
            e_mastery_4 INTEGER,
            e_endurance_4 INTEGER,
            food_briquette_12 INTEGER,
            e_mastery_17 INTEGER,
            e_endurance_17 INTEGER,
            e_mastery_24_1 INTEGER,
            e_endurance_24_1 INTEGER,
            e_mastery_24_2 INTEGER,
            e_endurance_24_2 INTEGER,
            flag24 INTEGER,
            e_mastery_35 INTEGER,
            e_endurance_35 INTEGER,
            zodiac_47 INTEGER,
            sword INTEGER,
            rat_bite INTEGER,
            e_mastery_55 INTEGER,
            e_endurance_55 INTEGER,
            appointment_74 INTEGER,
            e_mastery_82 INTEGER,
            e_endurance_82 INTEGER,
            e_mastery_84 INTEGER,
            e_endurance_84 INTEGER,
            e_mastery_104 INTEGER,
            e_endurance_104 INTEGER,
            e_mastery_106 INTEGER,
            e_endurance_106 INTEGER,
            e_mastery_107 INTEGER,
            e_endurance_107 INTEGER,
            dogfight_107 INTEGER,
            sealed_tube_110 INTEGER,
            magnetic_mine_110 INTEGER,
            grenade_110_215 INTEGER,
            hand_phaser_110 INTEGER,
            scanner_110_117 INTEGER,
            buttons_data_110 TEXT,
            e_mastery_113_1 INTEGER,
            e_endurance_113_1 INTEGER,
            e_mastery_113_2 INTEGER,
            e_endurance_113_2 INTEGER,
            flag113 INTEGER,
            bracelet_ziridium_117 INTEGER,
            e_mastery_124 INTEGER,
            e_endurance_124 INTEGER,
            e_mastery_133 INTEGER,
            e_endurance_133 INTEGER,
            e_mastery_136 INTEGER,
            e_endurance_136 INTEGER,
            killed_145 INTEGER,
            e_mastery_150 INTEGER,
            e_endurance_150 INTEGER,
            check_152 INTEGER,
            uniform_155 INTEGER,
            e_mastery_157 INTEGER,
            e_endurance_157 INTEGER,
            e_mastery_161 INTEGER,
            e_endurance_161 INTEGER,
            e_mastery_165 INTEGER,
            e_endurance_165 INTEGER,
            button_172 INTEGER,
            e_mastery_172_1 INTEGER,
            e_endurance_172_1 INTEGER,
            e_mastery_172_2 INTEGER,
            e_endurance_172_2 INTEGER,
            flag172 INTEGER,
            e_mastery_179 INTEGER,
            e_endurance_179 INTEGER,
            e_mastery_190 INTEGER,
            e_endurance_190 INTEGER,
            flag190 INTEGER,
            flag190_2 INTEGER,
            attack_190 INTEGER,
            e_mastery_206 INTEGER,
            e_endurance_206 INTEGER,
            e_mastery_215 INTEGER,
            e_endurance_215 INTEGER,
            grenade_215 INTEGER,
            e_mastery_224 INTEGER,
            e_endurance_224 INTEGER,
            without_weapons INTEGER,
            e_mastery_234_1 INTEGER,
            e_endurance_234_1 INTEGER,
            e_mastery_234_2 INTEGER,
            e_endurance_234_2 INTEGER,
            flag234 INTEGER,
            number_238 INTEGER,
            e_mastery_243 INTEGER,
            e_endurance_243 INTEGER,
            sand243 INTEGER,
            rounds243 INTEGER,
            e_mastery_244_1 INTEGER,
            e_endurance_244_1 INTEGER,
            e_mastery_244_2 INTEGER,
            e_endurance_244_2 INTEGER,
            flag244 INTEGER,
            jetpack_253 INTEGER,
            p_366_or_295 INTEGER,
            e_mastery_289 INTEGER,
            e_endurance_289 INTEGER,
            column22 INTEGER,
            column23 INTEGER,
            column24 INTEGER,
            column25 INTEGER,
            column26 INTEGER,
            e_mastery_295 INTEGER,
            e_endurance_295 INTEGER,
            e_mastery_295_1 INTEGER,
            e_endurance_295_1 INTEGER,
            e_mastery_295_2 INTEGER,
            e_endurance_295_2 INTEGER,
            e_mastery_295_3 INTEGER,
            e_endurance_295_3 INTEGER,
            e_mastery_295_4 INTEGER,
            e_endurance_295_4 INTEGER,
            flag295 INTEGER,
            e_mastery_298 INTEGER,
            e_endurance_298 INTEGER,
            e_mastery_313 INTEGER,
            e_endurance_313 INTEGER,
            e_mastery_341 INTEGER,
            e_endurance_341 INTEGER,
            e_mastery_351 INTEGER,
            e_endurance_351 INTEGER,
            warder_355 INTEGER,
            brain_probe_355 INTEGER,
            buttons_data_355 TEXT,
            e_mastery_366 INTEGER,
            e_endurance_366 INTEGER,
            e_mastery_366_1 INTEGER,
            e_endurance_366_1 INTEGER,
            e_mastery_366_2 INTEGER,
            e_endurance_366_2 INTEGER,
            e_mastery_366_3 INTEGER,
            e_endurance_366_3 INTEGER,
            e_mastery_366_4 INTEGER,
            e_endurance_366_4 INTEGER,
            flag366 INTEGER,
            e_mastery_367 INTEGER,
            e_endurance_367 INTEGER,
            e_mastery_373 INTEGER,
            e_endurance_373 INTEGER,
            e_mastery_373_1 INTEGER,
            e_endurance_373_1 INTEGER,
            e_mastery_373_2 INTEGER,
            e_endurance_373_2 INTEGER,
            e_mastery_375 INTEGER,
            e_endurance_375 INTEGER,
            money382 INTEGER,
            stroboscope_382 INTEGER,
            manual_horn_382 INTEGER,
            skein_of_nylon_rope_382 INTEGER,
            can_of_motor_oil_382 INTEGER,
            personal_robot_382 INTEGER,
            buttons_data_382 TEXT,
            e_mastery_391 INTEGER,
            e_endurance_391 INTEGER,
            cutter393 INTEGER
        );
        '''

        # Execute the SQL statement to create the table
        cursor.execute(create_table_sql)

        # Commit the changes and close the database connection
        conn.commit()
        conn.close()


def insert_character_data(user_id, column1, character):
    # Call the function to create the database and table if they don't exist
    create_database_if_not_exists()

    # Establish a database connection
    db_file = 'Data/table_with_data.db'
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Insert character data into the database
    cursor.execute(
        "INSERT INTO table_with_data (user_id, Mastery, Endurance, Luck, text_number) VALUES (?, ?, ?, ?, ?)",
        (user_id, character.mastery, character.endurance, character.luck, column1))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


def insert_list_data(user_id, buttons_data, column_name):
    # Connect to the SQLite database
    connect = sqlite3.connect('Data/table_with_data.db')
    cursor = connect.cursor()

    # Convert the list to a string representation
    buttons_data_str = ', '.join(map(lambda x: f'"{x}"', buttons_data))

    # Insert the string into the table
    insert_query = f"UPDATE table_with_data SET {column_name} = ? WHERE user_id = ?"
    cursor.execute(insert_query, (buttons_data_str, user_id))

    # Commit the changes
    connect.commit()

    # Close the connection
    cursor.close()
    connect.close()


def insert_7_values(user_id, Mastery, Endurance, Luck, column1, column2, column3):
    try:
        connect = sqlite3.connect('Data/table_with_data.db')
        cursor = connect.cursor()
        cursor.execute(
            'INSERT INTO table_with_data (user_id, Mastery, Endurance, Luck, column1, column2, column3) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (user_id, Mastery, Endurance, Luck, column1, column2, column3))
        connect.commit()
    except sqlite3.Error as e:
        print("Error inserting data:", e)
    finally:
        if cursor:
            cursor.close()


def insert_user(user_id, word_id):
    connect = sqlite3.connect('Data/table_with_data.db')
    cursor = connect.cursor()
    cursor.execute('INSERT INTO table_with_data (word_id, user_id) VALUES (?, ?)', (word_id, user_id))
    connect.commit()
    cursor.close()


def update_character_endurance(user_id, endurance_column, endurance):
    db_file = 'Data/table_with_data.db'

    try:
        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()

            # Update character endurance in the database
            cursor.execute(f'UPDATE table_with_data SET {endurance_column}=? WHERE user_id=?', (endurance, user_id))

            conn.commit()

    except sqlite3.Error as e:
        print(f"Error updating character endurance in the database: {e}")

    finally:
        cursor.close()


def update_endurance_user(endurance, user_id):
    connect = sqlite3.connect('Data/table_with_data.db')
    cursor = connect.cursor()
    cursor.execute(f'UPDATE table_with_data SET Endurance="{endurance}" WHERE user_id={user_id}')
    connect.commit()
    cursor.close()


def update_add_enemy(user_id, mastery, endurance, mastery_column, endurance_column):
    connect = sqlite3.connect('Data/table_with_data.db')
    cursor = connect.cursor()

    update_query = f'UPDATE table_with_data SET {mastery_column}=? WHERE user_id=?'
    cursor.execute(update_query, (mastery, user_id))

    update_query = f'UPDATE table_with_data SET {endurance_column}=? WHERE user_id=?'
    cursor.execute(update_query, (endurance, user_id))

    connect.commit()
    cursor.close()


def update_luck(user_id, luck_column, luck):
    connect = sqlite3.connect('Data/table_with_data.db')
    cursor = connect.cursor()
    cursor.execute(f'UPDATE table_with_data SET {luck_column}="{luck}" WHERE user_id={user_id}')
    connect.commit()
    cursor.close()


def update_mastery_endurance_luck(user_id, character):
    try:
        connect = sqlite3.connect('Data/table_with_data.db')
        cursor = connect.cursor()

        # Use parameterized queries to update the values
        cursor.execute('UPDATE table_with_data SET Mastery = ?, Endurance = ?, Luck = ? WHERE user_id = ?',
                       (character.mastery, character.endurance, character.luck, user_id))

        connect.commit()
    except sqlite3.Error as e:
        print(f"Error updating data: {e}")
    finally:
        cursor.close()
        connect.close()


def update_one_value(user_id, column_name, value):
    connect = sqlite3.connect('Data/table_with_data.db')
    cursor = connect.cursor()
    cursor.execute(f'UPDATE table_with_data SET {column_name}="{value}" WHERE user_id={user_id}')
    connect.commit()
    cursor.close()


def update_two_values(user_id, column_name1, value1, column_name2, value2):
    try:
        # Use a context manager to handle connections and ensure proper resource cleanup
        with sqlite3.connect('Data/table_with_data.db') as connection:
            cursor = connection.cursor()

            # Use parameterized queries to prevent SQL injection
            query1 = f'UPDATE table_with_data SET {column_name1}=? WHERE user_id=?'
            cursor.execute(query1, (value1, user_id))

            query2 = f'UPDATE table_with_data SET {column_name2}=? WHERE user_id=?'
            cursor.execute(query2, (value2, user_id))

            # Commit the changes after both updates
            connection.commit()

    except sqlite3.Error as e:
        print(f"Error executing the query: {e}")


def retrieve_character_data(user_id):
    create_database_if_not_exists()
    db_file = 'Data/table_with_data.db'
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Retrieve character data from the database
    cursor.execute("SELECT Mastery, Endurance, Luck FROM table_with_data WHERE user_id = ?", (user_id,))
    data = cursor.fetchone()

    conn.close()

    return data


def retrieve_character_data_id(word_id):
    create_database_if_not_exists()
    db_file = 'Data/table_with_data.db'
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Retrieve character data from the database
    cursor.execute("SELECT Mastery, Endurance, Luck FROM table_with_data WHERE word_id = ?", (word_id,))
    data = cursor.fetchone()

    conn.close()

    return data


def retrieve_creature_data(user_id, mastery_column, endurance_column):
    create_database_if_not_exists()
    db_file = 'Data/table_with_data.db'
    try:
        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()

            # Retrieve character data from the database
            cursor.execute(f"SELECT {mastery_column}, {endurance_column} FROM table_with_data WHERE user_id = ?",
                           (user_id,))
            data = cursor.fetchone()

            # Ensure a default value (0) for the third column
            result = data + (0,) if data else (0, 0, 0)

        return result

    except sqlite3.Error as e:
        print(f"Error retrieving data from the database: {e}")
        return (0, 0, 0)


def retrieve_character_data_2(column1):
    create_database_if_not_exists()
    db_file = 'Data/table_with_data.db'
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Retrieve character data from the database
    cursor.execute("SELECT Mastery, Endurance, Luck FROM table_with_data WHERE column1 = ?", (column1,))
    data = cursor.fetchone()

    conn.close()

    return data


def clear_cell(user_id, column_name):
    connect = sqlite3.connect('Data/table_with_data.db')
    cursor = connect.cursor()

    # Execute the update statement
    update_query = f"UPDATE table_with_data SET {column_name} = NULL WHERE user_id = ?"
    cursor.execute(update_query, (user_id,))

    # Commit the changes
    connect.commit()

    # Close the connection
    cursor.close()
    connect.close()


def clear_row_by_id(id_value):
    # Connect to the SQLite database
    connect = sqlite3.connect('Data/table_with_data.db')
    cursor = connect.cursor()

    # Execute the delete statement
    delete_query = f"DELETE FROM table_with_data WHERE user_id = ?"
    cursor.execute(delete_query, (id_value,))

    # Commit the changes
    connect.commit()

    # Close the connection
    cursor.close()
    connect.close()


def get_all_values():
    connect = sqlite3.connect('Data/table_with_data.db')
    cursor = connect.cursor()
    cursor.execute('SELECT * FROM table_with_data')
    res = cursor.fetchall()
    print(res)
    cursor.close()


def get_one_row(number):
    connect = sqlite3.connect('Data/table_with_data.db')
    cursor = connect.cursor()
    cursor.execute(f'SELECT * FROM table_with_data LIMIT 1 OFFSET {number - 1}')
    res = list(cursor.fetchone())
    cursor.close()
    return res


def get_unique_values(column_name):
    # Connect to the SQLite database
    conn = sqlite3.connect('Data/table_with_data.db')
    cursor = conn.cursor()

    # Execute a query to retrieve unique values from the specified column
    query = f"SELECT DISTINCT {column_name} FROM table_with_data"
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


def get_values_if_conditions(column_name_1, column_name_2):
    # Call the function to create the database and table if they don't exist
    create_database_if_not_exists()

    # Continue with your existing code to retrieve data from the database
    db_file = 'Data/table_with_data.db'
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    threshold_date = time.time()
    print(threshold_date, 'get_values_if_conditions на DB')

    query = f"SELECT DISTINCT {column_name_1} FROM table_with_data WHERE {column_name_2} < ?"
    cursor.execute(query, (threshold_date,))
    results = cursor.fetchall()

    conn.close()

    user_id_list = [user_id[0] for user_id in results]

    print(user_id_list, 'get_values_if_conditions/DB.py')
    return user_id_list


def get_username0(userid):
    connect = sqlite3.connect('Data/test.db')
    cursor = connect.cursor()
    cursor.execute(f'SELECT username FROM users WHERE userid={userid}')
    res = cursor.fetchall()
    print(res)
    cursor.close()


def get_username(user_id):
    connect = sqlite3.connect('Data/table_with_data.db')
    cursor = connect.cursor()
    cursor.execute(f'SELECT user_id FROM table_with_data WHERE user_id=?', (user_id,))
    res = cursor.fetchall()
    cursor.close()
    try:
        t = res[0]
        return True
    except:
        return False


def check_column_existence(column_name):
    conn = sqlite3.connect('Data/table_with_data.db')
    cursor = conn.cursor()

    # Check if the column exists in the table's schema
    cursor.execute(f"PRAGMA table_info(table_with_data)")
    columns = cursor.fetchall()

    for col_info in columns:
        if col_info[1] == column_name:
            return True  # Column exists

    conn.close()
    return False  # Column doesn't exist


# Example usage
# db_file = 'Data/table_with_data.db'
# table_name = 'table_with_data.db'
# column_name = '382_robot'
#
# if check_column_existence(db_file, table_name, column_name):
#     print(f"The column '{column_name}' exists.")
# else:
#     print(f"The column '{column_name}' does not exist.")

# def select_one_value(id, column_name1, column_name2):
#     connect = sqlite3.connect('Data/table_with_data.db')
#     cursor = connect.cursor()
#     cursor.execute(f'SELECT {column_name1} FROM table_with_data WHERE {column_name2}=?', (id,))
#     res = cursor.fetchall()
#     cursor.close()

def select_one_value(id, column_name1, column_name2):
    try:
        # Use a context manager to handle connections and ensure proper resource cleanup
        with sqlite3.connect('Data/table_with_data.db') as connection:
            cursor = connection.cursor()

            # Use parameterized queries to prevent SQL injection
            query = f'SELECT {column_name1} FROM table_with_data WHERE {column_name2}=?'
            cursor.execute(query, (id,))

            # Fetch one result instead of all, as you're selecting one value
            result = cursor.fetchone()

            # Check if a result is found before closing the cursor
            if result is not None:
                return result[0]  # Return the first (and only) value from the result

    except sqlite3.Error as e:
        print(f"Error executing the query: {e}")

    # Return a default value or handle the case when no result is found
    return None


def is_cell_not_empty(user_id, column_name):
    db_file = 'Data/table_with_data.db'

    try:
        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()

            # Check if a cell is not empty for the given user_id
            cursor.execute(
                f'SELECT 1 FROM Data/table_with_data WHERE user_id=? AND {column_name} IS NOT NULL AND {column_name} <> ""',
                (user_id,))
            result = cursor.fetchone()

            return result is not None

    except sqlite3.Error as e:
        print(f"Error checking if money382 is not empty: {e}")
        return False

    finally:
        cursor.close()


def get_value_universal(level, user_id, word_id):
    connect = sqlite3.connect('Data/clients_id.db')
    cursor = connect.cursor()
    cursor.execute(f'SELECT {level} FROM table_with_data WHERE {user_id}=?', (word_id,))
    res = cursor.fetchall()
    cursor.close()


def count_rows_in_database():
    # Connect to the database
    connect = sqlite3.connect('Data/table_with_data.db')

    # Create a cursor object to execute SQL queries
    cursor = connect.cursor()

    # Execute the query to count the rows
    cursor.execute(f'SELECT COUNT(*) FROM table_with_data')

    # Fetch the result of the query
    row_count = cursor.fetchone()[0]

    # Close the cursor and the database connection
    cursor.close()
    connect.close()

    # Return the row count
    return row_count


def count_rows_with_value(value):
    # Connect to the database
    conn = sqlite3.connect('Data/table_with_data.db')

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Execute the SELECT COUNT(*) query
    cursor.execute(f"SELECT COUNT(*) FROM table_with_data WHERE user_id = ?", (value,))

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
    conn = sqlite3.connect('Data/table_with_data.db')

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Execute the SELECT COUNT(*) query
    cursor.execute(f"SELECT COUNT(*) FROM table_with_data WHERE {column1_name} = ? AND {column2_name} = ?",
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
    conn = sqlite3.connect('Data/table_with_data.db')

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Execute the DELETE query to remove rows with empty cells
    cursor.execute(f"DELETE FROM table_with_data WHERE {column_name} IS NULL OR {column_name} = ''")

    # Commit the transaction to save the changes
    conn.commit()

    # Close the cursor and the database connection
    cursor.close()
    conn.close()
