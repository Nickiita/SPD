import sqlite3
import os


class SoundpadDatabase:
    def __init__(self, db_name):
        self.db_name = db_name
        categories = ['citation', 'gratitude', 'notifications', 'parting', 'request', 'welcome', 'melody']
        self.populate_database(categories)

    def create_tables(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sounds (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_id INTEGER,
                name TEXT NOT NULL,
                file_name TEXT NOT NULL,
                FOREIGN KEY (category_id) REFERENCES categories(id)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS hotkeys (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sound_id INTEGER,
                hotkey TEXT,
                FOREIGN KEY (sound_id) REFERENCES sounds(id)
            )
        ''')

        conn.commit()
        conn.close()

    def populate_database(self, categories):
        self.create_tables()

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('SELECT COUNT(*) FROM categories')
        if cursor.fetchone()[0] == 0:

            for category in categories:
                cursor.execute('INSERT INTO categories (name) VALUES (?)', (category,))

        cursor.execute('SELECT COUNT(*) FROM sounds')
        if cursor.fetchone()[0] == 0:

            for category in categories:
                sound_folder = os.path.join('..', 'resources', 'sounds', category)

                sound_files = os.listdir(sound_folder)
                for sound_file in sound_files:
                    file_name = os.path.join(sound_folder, sound_file)
                    cursor.execute(
                        'INSERT INTO sounds (category_id, name, file_name) VALUES ((SELECT id FROM categories WHERE name=?), ?, ?)',
                        (category, sound_file.split('.')[0], file_name))

        conn.commit()
        conn.close()

    def get_categories(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT name FROM categories')
        categories = [row[0] for row in cursor.fetchall()]
        conn.close()
        return categories

    def get_sounds_by_category(self, category):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(
            'SELECT name, file_name FROM sounds WHERE category_id = (SELECT id FROM categories WHERE name = ?)',
            (category,))
        sounds = cursor.fetchall()
        conn.close()
        return sounds
