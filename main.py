import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv
import os
from concurrent.futures import ThreadPoolExecutor, as_completed


def get_categories(base_url):
    """
    Récupère toutes les catégories de livres disponibles sur le site.
    Renvoie un dictionnaire avec le nom de la catégorie comme clé et l'URL de la catégorie comme valeur.
    """
    response = requests.get(base_url)
    if response.status_code != 200:
        return {}

    soup = BeautifulSoup(response.content, "html.parser")
    category_section = soup.find("ul", class_="nav nav-list")
    categories = {}
    if category_section:
        category_links = category_section.find_all("a")
        for link in category_links:
            category_name = link.get_text(strip=True)
            category_href = link.get("href")
            if category_href and category_name != 'Books':
                category_url = urljoin(base_url, category_href)
                categories[category_name] = category_url
    return categories


def get_links(category_url):
    """
    Récupère tous les liens des livres de toutes les pages de la catégorie donnée.
    """
    articles_links = []

    while True:
        response = requests.get(category_url)
        if response.status_code != 200:
            break  # Arrête si la page ne peut pas être récupérée

        soup = BeautifulSoup(response.content, "html.parser")
        articles = soup.find_all("article", class_="product_pod")

        # Récupération des liens sur la page actuelle
        for article in articles:
            a_tag = article.find("a")
            if a_tag and 'href' in a_tag.attrs:
                relative_href = a_tag['href']
                absolute_href = urljoin(category_url, relative_href)
                # Nettoyer l'URL en supprimant les segments '../' si présents
                absolute_href = absolute_href.replace('../../../', '')
                full_url = urljoin(
                    "http://books.toscrape.com/catalogue/", absolute_href)
                articles_links.append(full_url)

        # Vérification de la présence d'une page suivante
        next_button = soup.find("li", class_="next")
        if next_button:
            next_link = next_button.find("a")["href"]
            category_url = urljoin(category_url, next_link)
        else:
            break  # Pas de page suivante, sortie de la boucle

    return articles_links


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


def get_book_details(link):
    """
    Récupère les détails d'un livre à partir de son lien et renvoie un dictionnaire contenant les informations.
    """
    response = requests.get(link)
    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.content, "html.parser")

    # Titre
    title = soup.find("h1").get_text()

    # Tableau des informations produit
    product_table = soup.find("table", class_="table table-striped")
    product_info = {}
    if product_table:
        rows = product_table.find_all("tr")
        for row in rows:
            header = row.find("th").get_text()
            value = row.find("td").get_text()
            product_info[header] = value

    upc = product_info.get("UPC", "")
    price_including_tax = product_info.get("Price (incl. tax)", "")
    price_excluding_tax = product_info.get("Price (excl. tax)", "")
    availability = product_info.get("Availability", "").strip()
    number_available = extract_number(availability)

    # Description du produit
    description = ""
    desc_header = soup.find("div", id="product_description")
    if desc_header:
        desc_paragraph = desc_header.find_next_sibling("p")
        if desc_paragraph:
            description = desc_paragraph.get_text().strip()

    # Catégorie
    category = ""
    breadcrumb = soup.find("ul", class_="breadcrumb")
    if breadcrumb:
        category_links = breadcrumb.find_all("a")
        if len(category_links) >= 3:
            category = category_links[2].get_text().strip()

    # Note de l'avis
    rating = ""
    rating_tag = soup.find("p", class_="star-rating")
    if rating_tag:
        classes = rating_tag.get("class", [])
        for cls in classes:
            if cls != "star-rating":
                rating = cls
                break

    # URL de l'image
    image_url = ""
    img_tag = soup.find("img")
    if img_tag and 'src' in img_tag.attrs:
        relative_image_url = img_tag['src']
        image_url = urljoin(link, relative_image_url)

    # Créer un dictionnaire avec les informations requises
    book = {
        "product_page_url": link,
        "universal_product_code (upc)": upc,
        "title": title,
        "price_including_tax": price_including_tax,
        "price_excluding_tax": price_excluding_tax,
        "number_available": number_available,
        "product_description": description,
        "category": category,
        "review_rating": rating,
        "image_url": image_url
    }

    return book


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


def download_images(books_data):
    """
    Télécharge les images des livres en parallèle.
    """
    with ThreadPoolExecutor(max_workers=200) as executor:
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
                    f'Erreur lors du téléchargement de l\'image pour {book["title"]}: {exc}')


def get_details(articles_links):
    """
    Récupère les détails des livres en parallèle.
    """
    books_data = []

    with ThreadPoolExecutor(max_workers=200) as executor:
        future_to_url = {executor.submit(
            get_book_details, link): link for link in articles_links}

        for future in as_completed(future_to_url):
            link = future_to_url[future]
            try:
                book_details = future.result()
                if book_details:
                    books_data.append(book_details)
            except Exception as exc:
                print(f'Erreur lors du traitement de {link}: {exc}')
    return books_data


def main():
    # URL de la page d'accueil
    base_url = "http://books.toscrape.com/"

    # Récupération de toutes les catégories
    categories = get_categories(base_url)

    # Pour chaque catégorie, récupérer les liens des livres et les détails
    for category_name, category_url in categories.items():
        print(f"Traitement de la catégorie : {category_name}")
        articles_links = get_links(category_url)

        # Récupérer les détails des livres en parallèle
        books_data = get_details(articles_links)

        # Sauvegarder les données dans un fichier CSV nommé après la catégorie
        save_to_csv(books_data, category_name)

        # Télécharger les images en parallèle
        download_images(books_data)

        print(f"Catégorie {category_name} traitée avec succès.\n")


if __name__ == "__main__":
    main()
