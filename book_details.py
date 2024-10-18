import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor, as_completed
from utils import extract_number


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


def get_details(articles_links, max_workers):
    """
    Récupère les détails des livres en parallèle.
    """
    books_data = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
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
