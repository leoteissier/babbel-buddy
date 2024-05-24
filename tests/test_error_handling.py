import unittest
from src.config import OPENAI_API_KEY
from src.ai_manager import async_converse_with_ia
from src.history_manager import HistoryManager
from src.conversation_manager import ConversationManager


class TestErrorHandling(unittest.TestCase):
    def test_async_converse_with_ia_invalid_api_key(self):
        # Utiliser un try/except pour capturer l'erreur liée à une clé API invalide
        def callback(response):
            self.assertEqual(response, "Sorry, I am unable to respond at the moment.")

        # Sauvegarder l'ancienne clé API et la remplacer par une clé invalide
        original_api_key = OPENAI_API_KEY
        try:
            # Remplacer la clé API par une clé invalide
            globals()['OPENAI_API_KEY'] = "invalid_key"
            async_converse_with_ia("Hello", "English", callback)
        finally:
            # Restaurer l'ancienne clé API
            globals()['OPENAI_API_KEY'] = original_api_key

    def test_history_manager_database_error(self):
        history_manager = HistoryManager(':memory:')

        # Simuler une erreur de base de données en fermant la connexion
        history_manager.connection.close()

        with self.assertRaises(Exception):
            history_manager.save_conversation('Test Conversation', 'en', 'fr')

    def test_conversation_manager_start_new_conversation_error(self):
        history_manager = HistoryManager(':memory:')
        conversation_manager = ConversationManager(history_manager)

        # Simuler une erreur en fermant la connexion de l'historique
        history_manager.connection.close()

        with self.assertRaises(Exception):
            conversation_manager.start_new_conversation('English', 'French')


if __name__ == '__main__':
    unittest.main()
