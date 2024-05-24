import unittest
import os
import sqlite3
from src.history_manager import HistoryManager


class TestHistoryManager(unittest.TestCase):
    def setUp(self):
        # Setup a test database
        self.test_db = 'test_conversation_history.db'
        self.history_manager = HistoryManager(self.test_db)

    def tearDown(self):
        # Remove the test database
        os.remove(self.test_db)

    def test_save_conversation(self):
        conversation_id = self.history_manager.save_conversation('Test Conversation', 'English', 'English')
        self.assertIsNotNone(conversation_id)

    def test_get_all_conversations(self):
        self.history_manager.save_conversation('Test Conversation 1', 'English', 'English')
        self.history_manager.save_conversation('Test Conversation 2', 'French', 'French')
        conversations = self.history_manager.get_all_conversations()
        self.assertEqual(len(conversations), 2)

    def test_get_conversation_history(self):
        conversation_id = self.history_manager.save_conversation('Test Conversation', 'English', 'English')
        self.history_manager.save_message(conversation_id, 'Hello', 'user')
        history = self.history_manager.get_conversation_history(conversation_id)
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0][0], 'Hello')
        self.assertEqual(history[0][1], 'user')

    def test_delete_conversation(self):
        conversation_id = self.history_manager.save_conversation('Test Conversation', 'English', 'English')
        self.history_manager.delete_conversation(conversation_id)
        conversations = self.history_manager.get_all_conversations()
        self.assertEqual(len(conversations), 0)


if __name__ == '__main__':
    unittest.main()
