import tkinter as tk
from tkinter import messagebox, simpledialog


class ConversationList(tk.Frame):
    def __init__(self, parent, history_manager, load_conversation_history, display_widget):
        super().__init__(parent)
        self.history_manager = history_manager
        self.load_conversation_history = load_conversation_history
        self.display_widget = display_widget
        self.grid(sticky='nsew')
        self.populate_list()

    def populate_list(self):
        conversations = self.history_manager.get_all_conversations()
        self.delete_all_widgets()
        for conv_id, name in conversations:
            self.add_conversation_item({'id': conv_id, 'name': name})

    def delete_all_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()

    def add_conversation_item(self, conversation):
        frame = tk.Frame(self, borderwidth=1, relief="solid")
        frame.grid(sticky="ew")

        label = tk.Label(frame, text=conversation['name'])
        label.pack(side='left', fill='both', expand=True)

        load_button = tk.Button(frame, text="Load", command=lambda: self.load_conversation(conversation['id']))
        edit_button = tk.Button(frame, text="Edit", command=lambda: self.edit_conversation(conversation['id']))
        delete_button = tk.Button(frame, text="Delete", command=lambda: self.delete_conversation(conversation['id']))
        load_button.pack(side='right')
        edit_button.pack(side='right')
        delete_button.pack(side='right')

    def refresh(self):
        self.populate_list()

    def load_conversation(self, conv_id):
        self.load_conversation_history(conv_id)

    def edit_conversation(self, conv_id):
        new_name = simpledialog.askstring("Edit Conversation", "Enter new conversation name:")
        if new_name:
            self.history_manager.update_conversation_name(conv_id, new_name)
            self.refresh()

    def delete_conversation(self, conv_id):
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this conversation?"):
            self.history_manager.delete_conversation(conv_id)
            self.refresh()
            if hasattr(self.display_widget,
                       'current_conversation_id') and self.display_widget.current_conversation_id == conv_id:
                self.display_widget.current_conversation_id = None
                self.display_widget.conversation_text.config(state='normal')
                self.display_widget.conversation_text.delete(1.0, 'end')
                self.display_widget.conversation_text.config(state='disabled')
