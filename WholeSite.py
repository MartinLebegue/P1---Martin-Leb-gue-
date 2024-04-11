
import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin
import os
import re


fichier_text = r"C:\Users\33695\Desktop\Code\P1\infos_produits.txt"
fichier_text = 'infos_produits.txt'


def clean_name(name):
    return re.sub(r'[\\/*?:"<>|]', "", name).replace(' ', '_').replace('/', '_')


def scrap_infos(book_url):

    infos_produit = {}

    response = requests.get(book_url)
    if response.status_code == 200:
        print("Réponse HTTP réussie.")
    else:
        print(f"Erreur HTTP : {response.status_code}")
        return {}

    infos_produit["Product Page URL"] = book_url

    soup = BeautifulSoup(response.content, "html.parser")

    # Trouver le nom de la Catégorie via breadcrumb
    breadcrumb = soup.find('ul', class_='breadcrumb')
    links = breadcrumb.find_all('a')
    if links:
        category_link = links[-1]  # Avant-dernier lien
        category_name = category_link.text.strip()
    infos_produit["Catégorie"] = category_name

    # Trouver le titre via le selecteur h1 et l'ajouter au dictionnaire
    titre = soup.find("h1").text
    print("Titre ajouté au fichier texte.")
    titre_clean = clean_name(titre)  # Utilisation de la fonction clean_name pour nettoyer le titre
    infos_produit["Title"] = titre #Ajout au dictionnaire


    # Définir le chemin pour le dossier de catégorie
    category_path = os.path.join('images', category_name)
    os.makedirs(category_path, exist_ok=True)

    # Extraire l'URL de l'image
    image_tag = soup.find("div", class_='item active').find('img')
    if image_tag:
        image_url = urljoin(book_url, image_tag["src"])
        response_img = requests.get(image_url, timeout=10)  # 10 secondes de délai d'attente
        if response_img.status_code == 200:

            # Construire le chemin complet pour sauvegarder l'image avec le titre nettoyé
            img_filename = f"{titre_clean}.jpg"
            img_path = os.path.join(category_path, img_filename)
            with open(img_path, 'wb') as f:
                f.write(response_img.content)
            print(f"Image sauvegardée sous : {img_path}")
            infos_produit['Image Path'] = img_path


    # Trouver la description via l'id "product_description" et en déduire le "p" et l'écrire dans le dic
    div_description = soup.find("div", id="product_description")
    if div_description:
        # Trouver le paragraphe suivant le titre de la description
        p_description = div_description.find_next("p")
        if p_description:
            print("Description ajoutée au fichier texte.")
            infos_produit["Product Description"] = p_description.text

    # Trouver la balise <p> qui contient la classe 'star-rating'
    star_rating_element = soup.find("p", class_="star-rating")

    # Extraire le niveau de la note à partir de la classe
    if star_rating_element:

        # Les classes seront quelque chose comme 'star-rating Three'
        star_rating_classes = star_rating_element.get('class')  # ['star-rating', 'Three']

        # La classe de notation (par exemple, 'Three') est le deuxième élément de la liste
        star_rating = star_rating_classes[1] if len(star_rating_classes) > 1 else None

        # Convertir le texte de la note en nombre (par exemple 'Three' devient 3)
        ratings = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
        star_rating_number = ratings.get(star_rating, 0)
        print(f"Review out of 5 : {star_rating_number}")

        # Inscrire la review dans le fichier texte
        infos_produit["Review out of 5"] = star_rating_number

    #Trouver les valeurs dans le tableau descriptif

    tableau_produit = soup.find("table", class_="table table-striped")

    for row in tableau_produit.find_all("tr"):
        header = row.find("th").text
        value = row.find("td").text
        infos_produit[header] = value

    print("Informations extraites avec succès.")

    return infos_produit


# Récupère les infos de tous les livres présents sur une page d'une catégorie + Next Page URL
def scrape_category_page(category_url):
    response = requests.get(category_url)
    soup = BeautifulSoup(response.content, "html.parser")
    books_info = []

    books = soup.find_all('article', class_='product_pod')
    for book in books:
        book_link = book.find('h3').find('a')['href']
        full_book_link = urljoin(category_url, book_link)
        book_info = scrap_infos(full_book_link)
        books_info.append(book_info)

    next_link = soup.select_one('li.next > a')
    next_page_url = urljoin(category_url, next_link['href']) if next_link else None

    return books_info, next_page_url


# URL de la première page de la catégorie 'Fiction'
category_url = 'https://books.toscrape.com/catalogue/category/books/fiction_10/index.html'


def scrape_category(start_url):
    all_books_info = []
    category_url = start_url

    while category_url:
        books_info, next_page_url = scrape_category_page(category_url)
        all_books_info.extend(books_info)
        category_url = next_page_url  # Passer à la page suivante

    return all_books_info


# URL de départ pour la catégorie 'Fiction'
start_url = 'https://books.toscrape.com/catalogue/category/books/fiction_10/index.html'

# Scraping de toute la catégorie, y compris la gestion de la pagination
all_books_info = scrape_category(start_url)


def get_categories(home_url):
    response = requests.get(home_url)
    if response.status_code != 200:
        print("Erreur lors de la récupération de la page d'accueil")
        return []

    soup = BeautifulSoup(response.content, "html.parser")
    category_links = soup.select('div.side_categories > ul.nav.nav-list > li > ul > li > a')
    categories = {link.text.strip(): urljoin(home_url, link['href']) for link in category_links}

    return categories


def main():
    home_url = 'https://books.toscrape.com/index.html'
    categories = get_categories(home_url)

    for category_name, category_url in categories.items():
        print(f"Scraping books in category: {category_name}")
        all_books_info = scrape_category(category_url)

        if all_books_info:
            fichier_csv = f"infos_{category_name.replace(' ', '_')}.csv"
            with open(fichier_csv, mode='w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=all_books_info[0].keys())
                writer.writeheader()
                for book_info in all_books_info:
                    writer.writerow(book_info)
            print(f"Finished writing to {fichier_csv}")
        else:
            print(f"No books found in category: {category_name}")


if __name__ == "__main__":
    main()











