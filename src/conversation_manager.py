class ConversationManager:
    def __init__(self, history_manager):
        self.history_manager = history_manager
        self.conversation_counter = self.load_conversation_counter()

    @staticmethod
    def load_conversation_counter():
        try:
            with open("conversation_counter.txt", "r") as file:
                return int(file.read().strip())
        except FileNotFoundError:
            return 1

    def save_conversation_counter(self):
        with open("conversation_counter.txt", "w") as file:
            file.write(str(self.conversation_counter))

    def generate_conversation_id(self):
        self.conversation_counter += 1
        self.save_conversation_counter()
        return f"Conv {self.conversation_counter}"

    def start_new_conversation(self, current_language, native_language):
        conversation_name = "New Conversation"
        conversation_id = self.history_manager.save_conversation(conversation_name, current_language, native_language)
        return conversation_id
