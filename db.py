import sqlite3

# Function to create a SQLite database
def create_database(database_name):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS hashes (
                        id INTEGER PRIMARY KEY,
                        sha256 TEXT UNIQUE
                    )''')
    conn.commit()
    conn.close()

# Function to insert hashes into the database
def insert_hashes(database_name, hash_file):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    with open(hash_file, 'r') as file:
        for line in file:
            hash_value = line.strip()
            cursor.execute('INSERT OR IGNORE INTO hashes (sha256) VALUES (?)', (hash_value,))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    database_name = 'hashes.db'
    hash_file = 'sha256.txt'

    create_database(database_name)
    insert_hashes(database_name, hash_file)
