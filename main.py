from gui.main_window import MainWindow


def main():
    # Configuration basique pour la gestion des exceptions de Tkinter
    try:
        app = MainWindow()  # Crée l'instance de la fenêtre principale
        app.mainloop()  # Lance la boucle principale de l'interface utilisateur
    except Exception as e:
        print(f"An error occurred: {e}")  # Affiche les erreurs potentielles qui pourraient survenir
    finally:
        print("Application closed.")  # Message de confirmation que l'application est fermée proprement


if __name__ == "__main__":
    main()


