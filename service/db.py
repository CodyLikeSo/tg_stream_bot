import sqlite3

class Database:
    def __init__(self, db_name="mini_database.db"):
        self.db_name = db_name
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    telegram_id INTEGER UNIQUE,
                    username TEXT,
                    has_agreed INTEGER DEFAULT 0,
                    joined_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS stream (
                    id INTEGER PRIMARY KEY,
                    is_active INTEGER DEFAULT 0,
                    stream_url TEXT
                )
            """)
            cursor.execute("INSERT OR IGNORE INTO stream (id, is_active, stream_url) VALUES (1, 0, NULL)")
            conn.commit()

    def get_user_agreement(self, telegram_id: int):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT has_agreed FROM users WHERE telegram_id = ?", (telegram_id,))
            result = cursor.fetchone()
            return result[0] if result else None

    def add_user(self, telegram_id: int, username: str):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "INSERT INTO users (telegram_id, username, has_agreed) VALUES (?, ?, 0)", 
                    (telegram_id, username)
                )
                conn.commit()
            except sqlite3.IntegrityError:
                pass

    def agree_user(self, telegram_id: int):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET has_agreed = 1 WHERE telegram_id = ?", (telegram_id,))
            conn.commit()

    def set_stream_status(self, is_active: int, url: str = None):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            # Обновляем статус стрима
            cursor.execute("UPDATE stream SET is_active = ?, stream_url = ? WHERE id = 1", (is_active, url))
            
            # СБРОС АКТИВНОСТИ: при старте или остановке стрима отзываем согласие у всех
            cursor.execute("UPDATE users SET has_agreed = 0")
            conn.commit()

    def get_stream_info(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT is_active, stream_url FROM stream WHERE id = 1")
            return cursor.fetchone()

db = Database()