import os

from category import get_categories, get_links
from book_details import get_details
from data_saving import save_to_csv
from image_downloader import download_images


def main():
    # Afficher le nombre de coeurs CPU disponibles dans le PC
    cpu_count = os.cpu_count()
    print(f"Nombre de cœurs CPU disponibles : {cpu_count}")

    # Définir le nombre de threads à utiliser
    max_workers = cpu_count if cpu_count is not None else 1

    # URL de la page d'accueil
    base_url = "http://books.toscrape.com/"

    # Récupération de toutes les catégories
    categories = get_categories(base_url)

    # Pour chaque catégorie, récupérer les liens des livres et les détails
    for category_name, category_url in categories.items():
        print(f"Traitement de la catégorie : {category_name}")
        articles_links = get_links(category_url)

        # Récupérer les détails des livres en parallèle
        books_data = get_details(articles_links, max_workers)

        # Sauvegarder les données dans un fichier CSV nommé après la catégorie
        save_to_csv(books_data, category_name)

        # Télécharger les images en parallèle
        download_images(books_data, max_workers)

        print(f"Catégorie {category_name} traitée avec succès.\n")


if __name__ == "__main__":
    main()
