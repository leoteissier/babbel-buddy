import unittest
import tkinter as tk
from gui.main_window import MainWindow


class TestMainWindow(unittest.TestCase):
    def setUp(self):
        self.app = MainWindow()

    def tearDown(self):
        self.app.destroy()

    def test_main_window_creation(self):
        self.assertEqual(self.app.title(), "Babel Buddy")
        self.assertIsInstance(self.app.sidebar, tk.Frame)
        self.assertIsInstance(self.app.main_area, tk.Frame)
        self.assertIsInstance(self.app.conversation_text, tk.Text)

    def test_send_message(self):
        self.app.user_input.insert('end', 'Hello')
        self.app.send_message()
        self.assertIn('You: Hello', self.app.conversation_text.get(1.0, 'end'))


if __name__ == '__main__':
    unittest.main()
