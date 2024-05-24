import sqlite3


class HistoryManager:
    def __init__(self, db_name):
        """
        Initialize the HistoryManager with a database name and connect to the database.

        :param db_name: The name of the SQLite database file.
        """
        self.db_name = db_name
        self.connect()

    def connect(self):
        """
        Connect to the SQLite database and ensure the required tables exist.
        """
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self.ensure_table_exists()

    def ensure_table_exists(self):
        """
        Ensure that the necessary tables (conversations and messages) exist in the database.
        If they do not exist, create them.
        """
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
        """
        Add any missing columns to the tables if they do not already exist.
        This ensures backward compatibility with older versions of the database schema.
        """
        # Check and add missing columns to the 'conversations' table
        self.cursor.execute("PRAGMA table_info(conversations)")
        columns = [col[1] for col in self.cursor.fetchall()]
        if 'current_language' not in columns:
            self.cursor.execute("ALTER TABLE conversations ADD COLUMN current_language TEXT")
        if 'native_language' not in columns:
            self.cursor.execute("ALTER TABLE conversations ADD COLUMN native_language TEXT")

        # Check and add missing columns to the 'messages' table
        self.cursor.execute("PRAGMA table_info(messages)")
        columns = [col[1] for col in self.cursor.fetchall()]
        if 'sender' not in columns:
            self.cursor.execute("ALTER TABLE messages ADD COLUMN sender TEXT")

        self.connection.commit()

    def save_conversation(self, name, current_language, native_language):
        """
        Save a new conversation to the database.

        :param name: The name of the conversation.
        :param current_language: The current language of the conversation.
        :param native_language: The native language of the conversation.
        :return: The ID of the newly saved conversation.
        """
        try:
            self.cursor.execute("INSERT INTO conversations (name, current_language, native_language) VALUES (?, ?, ?)",
                                (name, current_language, native_language))
            self.connection.commit()
            return self.cursor.lastrowid
        except Exception as e:
            raise Exception(f"Failed to save conversation: {e}")

    def get_all_conversations(self):
        """
        Retrieve all conversations from the database.

        :return: A list of tuples containing the conversation IDs and names.
        """
        try:
            self.cursor.execute("SELECT id, name FROM conversations")
            return self.cursor.fetchall()
        except Exception as e:
            raise Exception(f"Failed to fetch conversations: {e}")

    def get_conversation_history(self, conversation_id):
        """
        Retrieve the message history for a given conversation.

        :param conversation_id: The ID of the conversation.
        :return: A list of tuples containing messages, senders, and timestamps.
        """
        try:
            self.cursor.execute(
                "SELECT message, sender, timestamp FROM messages WHERE conversation_id = ? ORDER BY timestamp ASC",
                (conversation_id,))
            return self.cursor.fetchall()
        except Exception as e:
            raise Exception(f"Failed to fetch conversation history: {e}")

    def save_message(self, conversation_id, message, sender):
        """
        Save a new message to the database.

        :param conversation_id: The ID of the conversation.
        :param message: The content of the message.
        :param sender: The sender of the message.
        """
        try:
            self.cursor.execute("INSERT INTO messages (conversation_id, message, sender) VALUES (?, ?, ?)",
                                (conversation_id, message, sender))
            self.connection.commit()
        except Exception as e:
            raise Exception(f"Failed to save message: {e}")

    def delete_conversation(self, conv_id):
        """
        Delete a conversation from the database.

        :param conv_id: The ID of the conversation to delete.
        """
        try:
            self.cursor.execute("DELETE FROM conversations WHERE id = ?", (conv_id,))
            self.connection.commit()
        except Exception as e:
            raise Exception(f"Failed to delete conversation: {e}")

    def update_conversation_name(self, conv_id, new_name):
        """
        Update the name of an existing conversation.

        :param conv_id: The ID of the conversation to update.
        :param new_name: The new name for the conversation.
        """
        try:
            self.cursor.execute("UPDATE conversations SET name = ? WHERE id = ?", (new_name, conv_id))
            self.connection.commit()
        except Exception as e:
            raise Exception(f"Failed to update conversation name: {e}")

    def __del__(self):
        """
        Ensure the database connection is closed when the HistoryManager is deleted.
        """
        if hasattr(self, 'connection'):
            self.connection.close()