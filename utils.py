def clean_filename(filename):
    """
    Remplace les caractères interdits dans un nom de fichier par des underscores.
    """
    invalid_chars = '\\/*?:"<>|'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename

def extract_number(text):
    """
    Extrait le premier nombre trouvé dans une chaîne de caractères.
    """
    number = ''
    for char in text:
        if char.isdigit():
            number += char
        elif number:
            break  # Arrête la boucle une fois le nombre terminé
    return number if number else '0'