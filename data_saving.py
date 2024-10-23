import csv
import os
from utils import clean_filename


def save_to_csv(books_data: list[dict], category_name: str) -> None:
    """
        Args:
            books_data (list[dict]): Liste de dictionnaires contenant les données des livres.
            category_name (str): Nom de la catégorie pour laquelle les données doivent être sauvegardées.

        Returns:
            None

    Sauvegarde les données des livres dans un fichier CSV spécifique à la catégorie dans le dossier de la catégorie.
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

    # Créer le dossier 'categories/<nom_catégorie>' s'il n'existe pas
    category_folder = os.path.join('categories', clean_filename(category_name))
    if not os.path.exists(category_folder):
        os.makedirs(category_folder)

    # Nom du fichier CSV
    filename = 'data.csv'
    file_path = os.path.join(category_folder, filename)

    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers, delimiter=';')
        writer.writeheader()
        for book in books_data:
            # Écrire seulement les champs spécifiés
            row = {field: book.get(field, '') for field in headers}
            writer.writerow(row)
