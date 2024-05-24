import threading
from openai import OpenAI
from src.config import OPENAI_API_KEY

client = OpenAI()


def define_ia_personality(language):
    """
    Define the personality of the AI based on the selected language.

    :param language: The language for the AI personality.
    :return: A string containing the personality message.
    """
    personalities = {
        "English": "I am here to help you learn English. How can I assist you today?",
        "French": "Je suis là pour vous aider à apprendre le français. Comment puis-je vous aider aujourd'hui?",
        "Deutsch": "Ich bin hier, um Ihnen beim Deutschlernen zu helfen. Wie kann ich Ihnen heute helfen?",
        "Spanish": "Estoy aquí para ayudarte a aprender español. ¿Cómo puedo asistirte hoy?",
    }
    return personalities.get(language, "Hello, how can I assist you today?")


def converse_with_ia(prompt, language):
    """
    Converse with the AI by sending a prompt and receiving a response.

    :param prompt: The user's message to the AI.
    :param language: The language in which the conversation is to be held.
    :return: The AI's response as a string.
    """
    try:
        # Check if the API key is available
        if not OPENAI_API_KEY:
            raise ValueError("OpenAI API key is missing. Please set it in the environment variable (.env)")

        # Check if the prompt is provided
        if not prompt:
            return "Sorry, I am unable to respond at the moment."

        # Check if the language is provided
        if not language:
            return "Sorry, I am unable to respond in the given language."

        # Define the AI personality based on the language
        personality = define_ia_personality(language)

        # Create the initial messages for the AI
        introduction = {"role": "system", "content": personality}
        user_message = {"role": "user", "content": prompt}

        # Initialize the OpenAI client
        client = OpenAI(api_key=OPENAI_API_KEY)

        # Create the chat completion request with the model and messages
        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[introduction, user_message]
        )

        # Return the AI's response
        return chat_completion.choices[0].message.content

    except Exception as e:
        print(f"Error communicating with OpenAI: {e}")
        return "Sorry, I am unable to respond at the moment."


def async_converse_with_ia(prompt, language, callback):
    """
    Handle the API request in a separate thread to avoid freezing the GUI.

    :param prompt: The user's message to the AI.
    :param language: The language in which the conversation is to be held.
    :param callback: A callback function to handle the AI's response.
    """

    def thread_function():
        """Thread function to handle the conversation and invoke the callback with the response."""
        response = converse_with_ia(prompt, language)
        callback(response)  # This callback function updates the GUI with the response

    # Start a new thread to handle the API request
    threading.Thread(target=thread_function).start()