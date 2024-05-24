import unittest
import os
from src.conversation_manager import ConversationManager
from src.history_manager import HistoryManager


class TestConversationManager(unittest.TestCase):
    def setUp(self):
        # Setup a test database
        self.test_db = 'test_conversation_history.db'
        self.history_manager = HistoryManager(self.test_db)
        self.conversation_manager = ConversationManager(self.history_manager)

    def tearDown(self):
        # Remove the test database
        os.remove(self.test_db)

    def test_start_new_conversation(self):
        conversation_id = self.conversation_manager.start_new_conversation('English', 'French')
        self.assertIsNotNone(conversation_id)

    def test_generate_conversation_id(self):
        conversation_id = self.conversation_manager.generate_conversation_id()
        self.assertTrue(conversation_id.startswith('Conv '))


if __name__ == '__main__':
    unittest.main()
