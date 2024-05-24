import sqlite3


class HistoryManager:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connect()

    def connect(self):
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self.ensure_table_exists()

    def ensure_table_exists(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                current_language TEXT,
                native_language TEXT
            )""")
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id INTEGER,
                message TEXT,
                sender TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(conversation_id) REFERENCES conversations(id)
            )""")
        self.connection.commit()
        self.add_missing_columns()

    def add_missing_columns(self):
        self.cursor.execute("PRAGMA table_info(conversations)")
        columns = [col[1] for col in self.cursor.fetchall()]
        if 'current_language' not in columns:
            self.cursor.execute("ALTER TABLE conversations ADD COLUMN current_language TEXT")
        if 'native_language' not in columns:
            self.cursor.execute("ALTER TABLE conversations ADD COLUMN native_language TEXT")
        self.cursor.execute("PRAGMA table_info(messages)")
        columns = [col[1] for col in self.cursor.fetchall()]
        if 'sender' not in columns:
            self.cursor.execute("ALTER TABLE messages ADD COLUMN sender TEXT")
        self.connection.commit()

    def save_conversation(self, name, current_language, native_language):
        try:
            self.cursor.execute("INSERT INTO conversations (name, current_language, native_language) VALUES (?, ?, ?)",
                                (name, current_language, native_language))
            self.connection.commit()
            return self.cursor.lastrowid
        except Exception as e:
            raise Exception(f"Failed to save conversation: {e}")

    def get_all_conversations(self):
        try:
            self.cursor.execute("SELECT id, name FROM conversations")
            return self.cursor.fetchall()
        except Exception as e:
            raise Exception(f"Failed to fetch conversations: {e}")

    def get_conversation_history(self, conversation_id):
        try:
            self.cursor.execute(
                "SELECT message, sender, timestamp FROM messages WHERE conversation_id = ? ORDER BY timestamp ASC",
                (conversation_id,))
            return self.cursor.fetchall()
        except Exception as e:
            raise Exception(f"Failed to fetch conversation history: {e}")

    def save_message(self, conversation_id, message, sender):
        try:
            self.cursor.execute("INSERT INTO messages (conversation_id, message, sender) VALUES (?, ?, ?)",
                                (conversation_id, message, sender))
            self.connection.commit()
        except Exception as e:
            raise Exception(f"Failed to save message: {e}")

    def delete_conversation(self, conv_id):
        try:
            self.cursor.execute("DELETE FROM conversations WHERE id = ?", (conv_id,))
            self.connection.commit()
        except Exception as e:
            raise Exception(f"Failed to delete conversation: {e}")

    def update_conversation_name(self, conv_id, new_name):
        try:
            self.cursor.execute("UPDATE conversations SET name = ? WHERE id = ?", (new_name, conv_id))
            self.connection.commit()
        except Exception as e:
            raise Exception(f"Failed to update conversation name: {e}")

    def __del__(self):
        if hasattr(self, 'connection'):
            self.connection.close()
