import subprocess

# Afficher une boîte de dialogue Zenity sur Linux (pour les bureaux basés sur GTK)
response = subprocess.run(['zenity', '--question', '--text', 'Voulez-vous vraiment quitter?', '--ok-label=Quitter', '--cancel-label=Annuler'], capture_output=True, text=True)

if response.returncode == 0:
    print("Vous avez choisi de quitter.")
    # Ajoutez ici le code pour effectuer l'action de fermeture de l'application
else:
    print("Vous avez annulé la fermeture de l'application.")
    # Ajoutez ici le code pour gérer l'annulation de la fermeture

