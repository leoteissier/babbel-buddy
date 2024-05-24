import threading

from openai import OpenAI
from src.config import OPENAI_API_KEY

client = OpenAI()


def define_instructions(language):
    """

    :param language:
    :return:
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

    :param language:
    :return:
    """
    client = OpenAI(api_key=OPENAI_API_KEY)

    instructions = define_instructions(language)

    assistant = client.beta.assistants.create(
        name=f"{language} Tutor",
        instructions=instructions,
        model="gpt-3-turbo",
    )

    # Create a thread for a new conversation
    thread = client.beta.threads.create()

    return thread, assistant


def add_message_and_get_response(thread_id, assistant_id, user_input):
    # Adding a message to the thread
    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=user_input
    )

    # Running the thread to get a response
    response = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id
    )

    return response.get("choices", [{}])[0].get('message', {}).get('content', '')


def async_converse_with_ia(prompt, language, callback):
    def thread_function():
        thread, assistant = converse_with_assistant(language)
        response = add_message_and_get_response(thread.id, assistant.id, prompt)
        callback(response)

    threading.Thread(target=thread_function).start()

