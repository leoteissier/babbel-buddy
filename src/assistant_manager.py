import threading
from openai import OpenAI
from src.config import OPENAI_API_KEY

client = OpenAI()


def define_instructions(language):
    """
    Define the personality and instructions for the AI assistant based on the selected language.

    :param language: The language in which the assistant should provide instructions.
    :return: A string containing the instructions for the assistant.
    """
    instructions = {
        "English": "You are a personal English tutor. Write and run code to answer questions in English.",
        "French": "Vous êtes un tuteur personnel de français. Écrivez et exécutez du code pour répondre aux questions en français.",
        "Deutsch": "Sie sind ein persönlicher Deutschlehrer. Schreiben und führen Sie Code aus, um Fragen auf Deutsch zu beantworten.",
        "Spanish": "Eres un tutor personal de español. Escribe y ejecuta código para responder preguntas en español."
    }
    return instructions.get(language, "Hello, how can I assist you today?")


def converse_with_assistant(language):
    """
    Create a new assistant and thread for conversation based on the selected language.

    :param language: The language in which the assistant should converse.
    :return: A tuple containing the thread and the assistant.
    """
    client = OpenAI(api_key=OPENAI_API_KEY)

    # Define the assistant's instructions based on the language
    instructions = define_instructions(language)

    # Create a new assistant with the specified instructions
    assistant = client.beta.assistants.create(
        name=f"{language} Tutor",
        instructions=instructions,
        model="gpt-3-turbo",
    )

    # Create a new conversation thread
    thread = client.beta.threads.create()

    return thread, assistant


def add_message_and_get_response(thread_id, assistant_id, user_input):
    """
    Add a message to the conversation thread and get a response from the assistant.

    :param thread_id: The ID of the conversation thread.
    :param assistant_id: The ID of the assistant.
    :param user_input: The user's input message.
    :return: The assistant's response message.
    """
    # Add the user's message to the thread
    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=user_input
    )

    # Run the thread to get a response from the assistant
    response = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id
    )

    # Return the content of the assistant's response message
    return response.get("choices", [{}])[0].get('message', {}).get('content', '')


def async_converse_with_ia(prompt, language, callback):
    """
    Handle the API request in a separate thread to avoid freezing the GUI.

    :param prompt: The user's message to the assistant.
    :param language: The language in which the conversation is to be held.
    :param callback: A callback function to handle the assistant's response.
    """

    def thread_function():
        # Create a new conversation and assistant based on the selected language
        thread, assistant = converse_with_assistant(language)
        # Add the user's message to the conversation and get the assistant's response
        response = add_message_and_get_response(thread.id, assistant.id, prompt)
        # Use the callback function to update the GUI with the assistant's response
        callback(response)

    # Start a new thread to handle the API request
    threading.Thread(target=thread_function).start()
