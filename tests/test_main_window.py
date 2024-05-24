import unittest
import tkinter as tk
from gui.main_window import MainWindow


class TestMainWindow(unittest.TestCase):

    def setUp(self):
        self.app = MainWindow()

    def test_setup_sidebar(self):
        self.app.setup_sidebar()
        self.assertIsNotNone(self.app.sidebar)

    def test_setup_main_area(self):
        self.app.setup_main_area()
        self.assertIsNotNone(self.app.main_area)

    def test_send_message(self):
        self.app.setup_main_area()
        self.app.user_input.insert('end', 'Hello, world!')
        self.app.send_message()
        content = self.app.conversation_text.get(1.0, 'end').strip()
        self.assertIn('You: Hello, world!', content)


if __name__ == '__main__':
    unittest.main()
