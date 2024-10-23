import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def get_categories(base_url: str) -> dict:
    """
    Retrieves all book categories available on the site.

    Args:
        base_url (str): The base URL of the book site.

    Returns:
        dict: A dictionary with the category name as the key and the category URL as the value.
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


def get_links(category_url: str) -> list:
    """
    Retrieves all book links from all pages of the given category using a for loop.

    Args:
        category_url (str): The URL of the book category.

    Returns:
        list: A list of links to the books in the category.
    """
    articles_links = []

    # Make an initial request to get the total number of pages
    response = requests.get(category_url)
    if response.status_code != 200:
        return articles_links  # Return an empty list if the page cannot be retrieved

    soup = BeautifulSoup(response.content, "html.parser")

    # Find the total number of pages
    page_count = 1  # By default, there is at least one page
    pagination = soup.find("ul", class_="pager")
    if pagination:
        current_page = pagination.find("li", class_="current")
        if current_page:
            text = current_page.get_text(strip=True)
            # The text is in the format "Page 1 of 4"
            parts = text.split()
            if "of" in parts:
                index_of_of = parts.index("of")
                page_count = int(parts[index_of_of + 1])

    # Generate the list of URLs for all pages
    page_urls = []
    base_page_url = category_url
    page_urls.append(base_page_url)
    for page_num in range(2, page_count + 1):
        # Construct the URL of the next page
        page_url = category_url.replace('index.html', f'page-{page_num}.html')
        page_urls.append(page_url)

    # Iterate over each page to retrieve book links
    for page_url in page_urls:
        response = requests.get(page_url)
        if response.status_code != 200:
            continue  # Skip to the next page if the page cannot be retrieved

        soup = BeautifulSoup(response.content, "html.parser")
        articles = soup.find_all("article", class_="product_pod")

        # Retrieve links on the current page
        for article in articles:
            a_tag = article.find("a")
            if a_tag and 'href' in a_tag.attrs:
                relative_href = a_tag['href']
                absolute_href = urljoin(page_url, relative_href)
                # Clean the URL by removing '../' segments if present
                absolute_href = absolute_href.replace('../../../', '')
                full_url = urljoin(
                    "http://books.toscrape.com/catalogue/", absolute_href)
                articles_links.append(full_url)

    return articles_links
