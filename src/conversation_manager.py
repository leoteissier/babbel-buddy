class ConversationManager:
    def __init__(self, history_manager):
        """
        Initialize the ConversationManager with a HistoryManager instance and load the conversation counter.

        :param history_manager: An instance of HistoryManager to handle conversation history.
        """
        self.history_manager = history_manager
        self.conversation_counter = self.load_conversation_counter()

    @staticmethod
    def load_conversation_counter():
        """
        Load the conversation counter from a file. If the file does not exist, return 1.

        :return: The current value of the conversation counter.
        """
        try:
            with open("conversation_counter.txt", "r") as file:
                return int(file.read().strip())
        except FileNotFoundError:
            return 1

    def save_conversation_counter(self):
        """
        Save the current value of the conversation counter to a file.
        """
        with open("conversation_counter.txt", "w") as file:
            file.write(str(self.conversation_counter))

    def generate_conversation_id(self):
        """
        Generate a new conversation ID by incrementing the conversation counter and saving it.

        :return: A new conversation ID in the format 'Conv {counter}'.
        """
        self.conversation_counter += 1
        self.save_conversation_counter()
        return f"Conv {self.conversation_counter}"

    def start_new_conversation(self, current_language, native_language):
        """
        Start a new conversation with the given languages and save it to the history manager.

        :param current_language: The current language of the conversation.
        :param native_language: The native language of the conversation.
        :return: The ID of the newly created conversation.
        """
        conversation_name = "New Conversation"
        conversation_id = self.history_manager.save_conversation(conversation_name, current_language, native_language)
        return conversation_id
