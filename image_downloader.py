import os
import requests
from utils import clean_filename
from concurrent.futures import ThreadPoolExecutor, as_completed


def download_image(image_url: str, category_name: str, image_name: str) -> None:
    """
    Télécharge l'image depuis l'URL donnée et l'enregistre dans le dossier 'photos/' de la catégorie.

    Args:
        image_url (str): L'URL de l'image à télécharger.
        category_name (str): Le nom de la catégorie dans laquelle enregistrer l'image.
        image_name (str): Le nom du fichier image à enregistrer.
    """
    response = requests.get(image_url)
    if response.status_code == 200:
        # Chemin du dossier 'photos/' dans le dossier de la catégorie
        photos_folder = os.path.join(
            'categories', clean_filename(category_name), 'photos')
        if not os.path.exists(photos_folder):
            os.makedirs(photos_folder)
        # Déterminer le chemin complet du fichier image
        image_path = os.path.join(photos_folder, image_name)
        # Écrire le contenu de l'image dans le fichier
        with open(image_path, 'wb') as file:
            file.write(response.content)


def download_images(books_data, max_workers):
    """
    Télécharge les images des livres en parallèle et les enregistre dans le dossier 'photos/' de la catégorie correspondante.
    """
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_book = {
            executor.submit(
                download_image,
                book["image_url"],
                book["category"],
                clean_filename(book["title"]) + ".jpg"
            ): book for book in books_data if book.get("image_url", "")
        }

        for future in as_completed(future_to_book):
            book = future_to_book[future]
            try:
                future.result()
            except Exception as exc:
                print(
                    f"Erreur lors du téléchargement de l'image pour {book['title']}: {exc}")
