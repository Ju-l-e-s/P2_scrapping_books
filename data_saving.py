import csv
import os
from utils import clean_filename


def save_to_csv(books_data, category_name):
    """
    Sauvegarde les données des livres dans un fichier CSV spécifique à la catégorie avec les champs spécifiés.
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

    # Créer le dossier 'csv_files' s'il n'existe pas
    if not os.path.exists('csv_files'):
        os.makedirs('csv_files')

    # Nettoyer le nom de la catégorie pour l'utiliser comme nom de fichier
    filename = clean_filename(category_name) + ".csv"
    file_path = os.path.join('csv_files', filename)

    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        for book in books_data:
            # Écrire seulement les champs spécifiés
            row = {field: book.get(field, '') for field in headers}
            writer.writerow(row)
