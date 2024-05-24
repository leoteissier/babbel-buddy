import unittest
import tkinter as tk
from gui.conversation_list import ConversationList
from src.history_manager import HistoryManager


class MockDisplayWidget:
    def __init__(self, root):
        self.current_conversation_id = None
        self.conversation_text = tk.Text(root)


class TestConversationList(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.history_manager = HistoryManager(':memory:')
        self.display_widget = MockDisplayWidget(self.root)
        self.conversation_list = ConversationList(self.root, self.history_manager, self.load_conversation_history,
                                                  self.display_widget)

    def load_conversation_history(self, conversation_id):
        pass  # Méthode factice pour les tests

    def test_add_conversation_item(self):
        conversation = {'id': 1, 'name': 'Test Conversation'}
        self.conversation_list.add_conversation_item(conversation)
        self.assertEqual(len(self.conversation_list.winfo_children()), 1)

    def test_delete_conversation(self):
        conversation = {'id': 1, 'name': 'Test Conversation'}
        self.history_manager.save_conversation(conversation['name'], 'en', 'en')
        self.conversation_list.add_conversation_item(conversation)
        self.conversation_list.delete_conversation(conversation['id'])
        self.assertEqual(len(self.conversation_list.winfo_children()), 0)


if __name__ == '__main__':
    unittest.main()
