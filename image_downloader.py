import os
import requests
from utils import clean_filename
from concurrent.futures import ThreadPoolExecutor, as_completed


def download_image(image_url, category, image_name):
    """
    Télécharge l'image depuis l'URL donnée et l'enregistre dans un dossier spécifique à la catégorie.
    """
    response = requests.get(image_url)
    if response.status_code == 200:
        # Créer le dossier pour la catégorie s'il n'existe pas
        category_folder = os.path.join('images', category)
        if not os.path.exists(category_folder):
            os.makedirs(category_folder)
        # Déterminer le chemin complet du fichier image
        image_path = os.path.join(category_folder, image_name)
        # Écrire le contenu de l'image dans le fichier
        with open(image_path, 'wb') as file:
            file.write(response.content)


def download_images(books_data, max_workers):
    """
    Télécharge les images des livres en parallèle.
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
