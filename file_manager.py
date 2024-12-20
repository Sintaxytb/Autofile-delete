import os
import shutil
import time
from pathlib import Path
from send2trash import send2trash


def analyze_file(file_path):
    """
    Analyze un simple fichier et affiche ses propriétés
    :param file_path: Full path to the file to analyze.
    """
    if not os.path.exists(file_path):
        print(f"Le fichier '{file_path}' il existe pas chef tia serré ou quoi?")
        return

    file_size = os.path.getsize(file_path)  # Taille en bytes
    file_extension = os.path.splitext(file_path)[1]
    last_access_time = time.ctime(os.path.getatime(file_path))  # Un format que les humains comprennent prck on est trop con sayer

    print(f"File Analysis:")
    print(f"Path: {file_path}")
    print(f"Size: {file_size} bytes")
    print(f"Extension: {file_extension}")
    print(f"Last Accessed: {last_access_time}")


def move_file_to_recycle_bin(file_path):
    """
    Move a specific file to the recycle bin.
    :param file_path: Full path to the file to move.
    """
    try:
        send2trash(file_path)
        print(f"Success: Le fichier '{file_path}' a ete envoyé a la poubelle.")
    except Exception as e:
        print(f"Error: Oups, ce n'est pas censé arriver, c'est arriver à cause de: {e}")


def move_old_files_to_temp(folder_path, days_threshold):
    """
    Detect files in a folder that have not been accessed for a given number of days
    and move them to a temporary folder.
    :param folder_path: Path to the folder to analyze.
    :param days_threshold: Number of days since last access to qualify as "old."
    """
    temp_folder = Path(os.getenv('TEMP')) / "Old_Files"
    temp_folder.mkdir(exist_ok=True)

    current_time = time.time()
    age_threshold = days_threshold * 86400  # Convertis les jours en secondes prck il comprend aps sinon ce con
    moved_files = []

    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                last_access_time = os.path.getatime(file_path)
                file_age = current_time - last_access_time

                if file_age > age_threshold:
                    target_path = temp_folder / os.path.relpath(file_path, folder_path)
                    target_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(file_path, target_path)
                    moved_files.append(file_path)
            except Exception as e:
                print(f"Error processing file {file}: {e}")

    if moved_files:
        print(f"J'ai bougé {len(moved_files)} ici: {temp_folder}")
        for f in moved_files:
            print(f" - {f}")
    else:
        print("C'est recent tout ça dit moi ?")


# Fonction principale pour combiner les fonctionnalités (pkoi je commente ça moi ???)
def main():
    print("Choisis ton destin:")
    print("1. Analyse un fichier specifique")
    print("2. Met un fichier specifique dans la poubelle")
    print("3. Met les fichiers specifiques dans un dossier temporaire")
    choice = input("Choisis aller j'ai pas tout ton temps (1/2/3): ")

    if choice == "1":
        file_path = input("Met tout le chemin du fichier frerot : ").strip()
        analyze_file(file_path)

    elif choice == "2":
        file_path = input("Azy donne le path, j'vais le graille : ").strip()
        if os.path.exists(file_path):
            analyze_file(file_path)  # Montre les détails (du fichiers pas de ta mère)
            confirm = input(f"T sûr tu veut bouger '{file_path}' a la poubelle ? (yes/no): ").strip().lower()
            if confirm == "yes":
                move_file_to_recycle_bin(file_path)
        else:
            print("Il existe pas ton fichier mon gars tié fou")

    elif choice == "3":
        folder_path = input("Envoie le path des fichiers a scanner ").strip()
        if os.path.exists(folder_path):
            days_threshold = int(
                input("Met le nombre de jours pour que ce soit qualifié de vieux (comme ton papy) ").strip())
            move_old_files_to_temp(folder_path, days_threshold)
        else:
            print("Il existe pas le fichier frr tia serré ?")

    else:
        print("J'en ai vu des cons mais toi... Ya marqué 1,2 et 3 pas 378 connard va")


# FAIS TOURNER LE MOTEUR MARCEL
if __name__ == "__main__":
    main()
