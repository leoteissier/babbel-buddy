import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Clé API unique pour ChatGPT
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OpenAI API key is missing. Please set it in the .env file")

# Dictionnaire pour mapper les numéros aux noms de langues
LANGUE_MAPPINGS = {
    'français': 'fr',
    'english': 'en',
    'espanol': 'es',
    'deutsch': 'de'
}