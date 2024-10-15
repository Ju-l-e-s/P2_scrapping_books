import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv

def get_links(base_url):
    """
    Récupère tous les liens des livres de toutes les pages de la catégorie donnée.
    """
    articles_links = []

    while True:
        response = requests.get(base_url)
        if response.status_code != 200:
            break  # Arrête si la page ne peut pas être récupérée

        soup = BeautifulSoup(response.content, "html.parser")
        articles = soup.find_all("article", class_="product_pod")

        # Récupération des liens sur la page actuelle
        for article in articles:
            a_tag = article.find("a")
            if a_tag and 'href' in a_tag.attrs:
                relative_href = a_tag['href']
                absolute_href = urljoin(base_url, relative_href)
                absolute_href = absolute_href.replace('../../../', '')
                full_url = "http://books.toscrape.com/catalogue/" + \
                    absolute_href.split("catalogue/")[-1]
                articles_links.append(full_url)

        # Vérification de la présence d'une page suivante
        next_button = soup.find("li", class_="next")
        if next_button:
            next_link = next_button.find("a")["href"]
            base_url = urljoin(base_url, next_link)
        else:
            break  # Pas de page suivante, sortie de la boucle

    return articles_links


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
    number_available = product_info.get("Availability", "").strip()
    # Extraire le nombre disponible à partir de la chaîne
    number_available = ''.join(filter(str.isdigit, number_available))

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

    # Créer un dictionnaire avec les informations
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


def get_details(articles_links):
    """
    Récupère les détails de chaque livre à partir de la liste des liens.
    """
    books_data = []

    for link in articles_links:
        book_details = get_book_details(link)
        if book_details:
            books_data.append(book_details)

    return books_data


def save_to_csv(books_data, filename="books_data.csv"):
    """
    Sauvegarde les données des livres dans un fichier CSV.
    """
    if not books_data:
        return

    headers = books_data[0].keys()

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(books_data)


if __name__ == "__main__":
    # URL de la page à scraper
    base_url = "http://books.toscrape.com/catalogue/category/books/historical-fiction_4/index.html"

    # Récupération des liens des livres avec pagination
    articles_links = get_links(base_url)
    print(f"Nombre total de liens récupérés : {len(articles_links)}")

    # Récupération des détails des livres
    books_data = get_details(articles_links)

    # Sauvegarde des données dans un fichier CSV
    save_to_csv(books_data)
    print("Données sauvegardées dans books_data.csv")
