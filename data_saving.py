import csv
import os
from typing import List, Dict
from utils import clean_filename


def save_to_csv(books_data: List[Dict[str, str]], category_name: str) -> None:
    """
    Sauvegarde les données des livres dans un fichier CSV spécifique à la catégorie dans le dossier de la catégorie.

    Args:
        books_data (List[Dict[str, str]]): Une liste de dictionnaires contenant les données des livres.
        category_name (str): Le nom de la catégorie pour laquelle les données doivent être sauvegardées.
    """
    if not books_data:
        return

    # Spécifier les champs dans l'ordre souhaité
    headers = [
        "product_page_url",
        "universal_product_code (upc)",
        "title",
        "price_including_tax",
        "price_excluding_tax",
        "number_available",
        "product_description",
        "category",
        "review_rating",
        "image_url"
    ]

    # Créer le répertoire pour la catégorie s'il n'existe pas
    category_dir = os.path.join('categories', clean_filename(category_name))
    os.makedirs(category_dir, exist_ok=True)

    # Chemin du fichier CSV
    csv_file_path = os.path.join(
        category_dir, f"{clean_filename(category_name)}.csv")

    # Écrire les données dans le fichier CSV
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writeheader()

        for book in books_data:
            # Écrire seulement les champs spécifiés
            row = {field: book.get(field, '') for field in headers}
            writer.writerow(row)
