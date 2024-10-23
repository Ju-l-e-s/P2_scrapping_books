def clean_filename(filename: str) -> str:
    """
    Remplace les caractères interdits dans un nom de fichier par des underscores.
    
    Arguments:
    filename (str): Le nom de fichier à nettoyer.
    
    Returns:
    str: Le nom de fichier nettoyé.
    """
    invalid_chars = '\\/*?:"<>|'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename

def extract_number(text: str) -> int:
    """
    Extrait le premier nombre trouvé dans une chaîne de caractères.
    
    Arguments:
    text (str): La chaîne de caractères à analyser.
    
    Returns:
    int: Le premier nombre trouvé dans la chaîne de caractères, ou 0 si aucun nombre n'est trouvé.
    """
    number = ''
    for char in text:
        if char.isdigit():
            number += char
        elif number:
            break  # Arrête la boucle une fois le nombre terminé
    return int(number) if number else 0