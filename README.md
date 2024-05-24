# Babel Buddy

Babel Buddy est un script Python offrant une opportunité unique de pratiquer une langue en interagissant avec l'API de ChatGPT. Il intègre une fonction de correction orthographique pour optimiser votre apprentissage.

## Fonctionnalités

- **Choix de Langue** : Pratiquez en Français, Anglais, Espagnol ou Allemand.
- **Correction Orthographique** : Corrections automatiques pour renforcer l'apprentissage.
- **Personnalisation de l'IA** : L'IA adapte sa réponse selon la langue sélectionnée.

## Prérequis

Avant de commencer, assurez-vous d'avoir installé :

- Python 3.12
- Bibliothèques Python : `openai`, `python-dotenv`, `pyspellchecker`
- Sphinx et extensions Sphinx (si nécessaire pour générer la documentation)

## Installation

1. Clonez le dépôt :

    ```bash
    git clone https://github.com/leoteissier/babbel-buddy.git
    cd babbel-buddy
    ```

2. Créez et activez un environnement virtuel :

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Sur macOS/Linux
    # ou
    venv\Scripts\activate  # Sur Windows
    ```

3. Installez les dépendances :

    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1. Créez un fichier `.env` à la racine du projet.
2. Ajoutez votre clé API OpenAI :

    ```dotenv
    OPENAI_API_KEY=your_openai_api_key_here
    ```

## Utilisation

Exécutez le script :

```bash
python3 main.py
```

Suivez les instructions pour choisir votre langue native et celle à pratiquer.

## Tests
Pour exécuter les tests, utilisez la commande suivante :

```bash
python3 -m unittest discover -s tests
```

## Documentation avec Sphinx

Ce projet utilise [Sphinx](http://www.sphinx-doc.org/en/master/) pour générer une documentation détaillée du code source. Sphinx est un outil qui facilite la création de documents intelligibles et beaux depuis le code source.

### Générer la Documentation

Pour générer la documentation en HTML, suivez ces étapes :

1. Assurez-vous d'avoir Sphinx installé, ainsi que toute extension requise. Vous pouvez installer Sphinx en utilisant pip :
    
```bash
pip install sphinx
```

2. Initialisez un projet Sphinx :
```bash
mkdir docs
cd docs
sphinx-quickstart
```

3. Accédez au dossier `source` dans le dossier `docs` :

```bash
cd docs/source
```

4. Exécutez la commande Sphinx pour construire les documents :

```bash
sphinx-build -b html . ../build
```

Cette commande générera une version HTML de la documentation dans le dossier `docs/build`.

### Consulter la Documentation

Après la génération, ouvrez le fichier `index.html` situé dans `docs/build/html` avec votre navigateur pour voir la documentation.


## Contribution

Contributions bienvenues. Pour proposer des améliorations, créez une pull request.

## Licence

Ce projet est sous licence [MIT](https://choosealicense.com/licenses/mit/).