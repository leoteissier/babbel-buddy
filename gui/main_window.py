import tkinter as tk
from PIL import Image, ImageTk
import os
import queue
import uuid

from gui.conversation_list import ConversationList
from src.conversation_manager import ConversationManager
from src.history_manager import HistoryManager
from src.config import LANGUE_MAPPINGS
from src.ai_manager import async_converse_with_ia
from src.spell_correction import spell_correction


class MainWindow(tk.Tk):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Babel Buddy")
        self.geometry("1000x600")
        self.minsize(400, 300)

        # Initialize Managers
        self.history_manager = HistoryManager('../conversation_history.db')
        self.conversation_manager = ConversationManager(self.history_manager)

        # Queue for database operations
        self.db_queue = queue.Queue()

        # Current conversation ID and message ID
        self.current_conversation_id = None
        self.message_ids = {}  # Dictionary to map message IDs to conversation IDs

        # Configure main layout
        self.configure_grid()

        # Setup Widgets
        self.setup_main_area()
        self.setup_sidebar()

        # Lier la touche Entrée à la méthode send_message
        self.user_input.bind('<Return>', self.send_message)

        # Start the loop to handle database operations
        self.process_db_queue()

    def configure_grid(self):
        self.sidebar = tk.Frame(self, bg='#333333', width=250)
        self.sidebar.grid(row=0, column=0, sticky="ns", padx=5)

        self.main_area = tk.Frame(self, bg='#444444')
        self.main_area.grid(row=0, column=1, sticky="nsew")

        self.grid_columnconfigure(0, weight=1, minsize=200)
        self.grid_columnconfigure(1, weight=4)
        self.grid_rowconfigure(0, weight=1)

    def setup_sidebar(self):
        self.conversation_list = ConversationList(
            self.sidebar,
            self.history_manager,
            self.load_conversation_history,
            self
        )
        self.conversation_list.grid(sticky="nsew")

        # New Conversation Button
        script_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(script_dir, "..", "assets", "new_conversation_icon.png")

        try:
            new_conv_image = Image.open(icon_path)
            new_conv_image = new_conv_image.resize((20, 20), Image.LANCZOS)
            new_conv_icon = ImageTk.PhotoImage(new_conv_image)

            self.new_conv_button = tk.Button(
                self.sidebar, text="New Conversation", image=new_conv_icon, compound="left",
                command=self.create_new_conversation
            )
            self.new_conv_button.image = new_conv_icon
            self.new_conv_button.grid(sticky="ew", pady=10)
        except Exception as e:
            print(f"An error occurred: {e}")
            print(f"Failed to load icon from path: {icon_path}")

    def setup_main_area(self):
        languages = list(LANGUE_MAPPINGS.keys())

        self.native_language_label = tk.Label(self.main_area, text="Native Language", bg='#444444', fg='white')
        self.language_label = tk.Label(self.main_area, text="Language", bg='#444444', fg='white')
        self.native_language = tk.StringVar(self.main_area)
        self.native_language.set('English')
        self.language = tk.StringVar(self.main_area)
        self.language.set('English')
        self.native_language_dropdown = tk.OptionMenu(self.main_area, self.native_language, *languages)
        self.language_dropdown = tk.OptionMenu(self.main_area, self.language, *languages)

        self.native_language_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')
        self.native_language_dropdown.grid(row=0, column=1, padx=10, pady=5, sticky='w')
        self.language_label.grid(row=1, column=0, padx=10, pady=5, sticky='w')
        self.language_dropdown.grid(row=1, column=1, padx=10, pady=5, sticky='w')

        self.conversation_text = tk.Text(self.main_area, bg='#555555', fg='white', wrap='word', state='disabled')
        self.conversation_text.grid(row=2, column=0, columnspan=2, sticky='nsew', padx=10, pady=10)

        self.user_input = tk.Text(self.main_area, height=3, bg='#666666', fg='white', wrap='word')
        self.user_input.grid(row=3, column=0, sticky='ew', padx=10, pady=10)
        self.send_button = tk.Button(
            self.main_area, text="Send", command=self.send_message,
            font=('Helvetica', 12, 'bold'),
            relief='raised',
            padx=10,
            pady=5
        )
        self.send_button.grid(row=3, column=1, padx=10, pady=10)

        self.main_area.grid_columnconfigure(0, weight=1)
        self.main_area.grid_rowconfigure(2, weight=1)

        # Adding tags for text alignment and spacing
        self.conversation_text.tag_configure('user', justify='right', spacing3=10)
        self.conversation_text.tag_configure('ai', justify='left', spacing3=10)
        self.conversation_text.tag_configure('professor', justify='left', spacing3=10)
        self.conversation_text.tag_configure('spacing', spacing1=10, spacing3=10)

    def process_db_queue(self):
        while not self.db_queue.empty():
            func, args = self.db_queue.get()
            func(*args)
        self.after(100, self.process_db_queue)  # Check the queue every 100ms

    def load_conversation_history(self, conversation_id):
        self.current_conversation_id = conversation_id
        conversation_history = self.history_manager.get_conversation_history(conversation_id)
        self.conversation_text.config(state='normal')
        self.conversation_text.delete(1.0, 'end')
        for message, sender, timestamp in conversation_history:
            if sender == 'user':
                self.conversation_text.insert('end', f"You: {message}\n", ('user', 'spacing'))
            elif sender == 'professor':
                self.conversation_text.insert('end', f"Professor: {message}\n", ('professor', 'spacing'))
            else:
                self.conversation_text.insert('end', f"AI: {message}\n", ('ai', 'spacing'))
        self.conversation_text.config(state='disabled')

    def send_message(self, event=None):
        message = self.user_input.get(1.0, 'end').strip()
        self.user_input.delete(1.0, 'end')
        if message:
            if not self.current_conversation_id:
                self.current_conversation_id = self.conversation_manager.start_new_conversation(
                    self.language.get(), self.native_language.get()
                )
                self.conversation_list.refresh()

            self.conversation_text.config(state='normal')
            self.conversation_text.insert('end', f"You: {message}\n", ('user', 'spacing'))
            self.conversation_text.config(state='disabled')
            self.db_queue.put((self.history_manager.save_message, (self.current_conversation_id, message, 'user')))
            corrected_message = spell_correction(message, self.language.get())
            if corrected_message != message:
                self.conversation_text.config(state='normal')
                self.conversation_text.insert('end', f"Professor: {corrected_message}\n", ('professor', 'spacing'))
                self.conversation_text.config(state='disabled')
                self.db_queue.put(
                    (self.history_manager.save_message, (self.current_conversation_id, corrected_message, 'professor')))

            message_id = str(uuid.uuid4())
            self.message_ids[message_id] = self.current_conversation_id
            async_converse_with_ia(corrected_message, self.language.get(),
                                   lambda response: self.update_conversation_text(response, message_id,
                                                                                  self.current_conversation_id))

    def update_conversation_text(self, response, message_id, conversation_id):
        self.db_queue.put((self.save_ai_response, (response, message_id, conversation_id)))

    def save_ai_response(self, response, message_id, conversation_id):
        if conversation_id in self.message_ids.values():
            self.conversation_text.config(state='normal')
            if conversation_id == self.current_conversation_id:
                self.conversation_text.insert('end', f"AI: {response}\n", ('ai', 'spacing'))
            self.conversation_text.config(state='disabled')
            self.history_manager.save_message(conversation_id, response, 'ai')
        del self.message_ids[message_id]

    def create_new_conversation(self):
        self.current_conversation_id = self.conversation_manager.start_new_conversation(
            self.language.get(), self.native_language.get()
        )
        self.conversation_list.refresh()
        self.conversation_text.config(state='normal')
        self.conversation_text.delete(1.0, 'end')  # Clear conversation text area
        self.conversation_text.config(state='disabled')