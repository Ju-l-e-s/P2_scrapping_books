import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


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
