import os
import sys
from category import get_categories, get_links
from book_details import get_details
from data_saving import save_to_csv
from image_downloader import download_images


def main():
    # Afficher le nombre de cœurs CPU disponibles
    cpu_count = os.cpu_count()
    print(f"Nombre de cœurs CPU disponibles : {cpu_count}")

    # Définir le nombre de threads à utiliser
    max_workers = cpu_count if cpu_count is not None else 1

    # URL de la page d'accueil
    base_url = "http://books.toscrape.com/"

    # Récupération de toutes les catégories
    category = get_categories(base_url)

    # Créer le dossier 'categories' s'il n'existe pas
    if not os.path.exists('categories'):
        os.makedirs('categories')

    # Pour chaque catégorie, récupérer les liens des livres et les détails
    for category_name, category_url in category.items():
        print(f"Traitement de la catégorie : {category_name}")
        articles_links = get_links(category_url)

        # Récupérer les détails des livres en parallèle
        books_data = get_details(articles_links, max_workers)

        # Sauvegarder les données dans un fichier CSV dans le dossier de la catégorie
        save_to_csv(books_data, category_name)

        # Télécharger les images en parallèle dans le dossier 'photos/' de la catégorie
        download_images(books_data, max_workers)

        print(f"Catégorie {category_name} traitée avec succès.\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nScript interrompu par l'utilisateur.")
        sys.exit(0)
